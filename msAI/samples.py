
"""msAI module to create a unified set of MS data samples paired with any additional metadata.

Features
    * Creation of a sample set from a directory of MS data files
    * Pairing of MS data and sample metadata
    * Extraction of sample metadata from csv files
    * Saving / loading data (serialization, compression, checksum)

Todo
    * init_ms mp logging calls
    * Create a msFile subclass form msAIr files - and move loading to that class

"""


import msAI
import msAI.msData as msData
from msAI.errors import SampleRunMSinitError
from msAI.miscUtils import Saver, MultiTaskDF
from msAI.miscDecos import log_timer
from msAI.types import Series

import logging
import os
from functools import partial

import pandas as pd


logger = logging.getLogger(__name__)
"""Module logger."""


class SampleSet:
    """Class to create a dataframe of a set of SampleRuns created from a MSfileSet and paired with 0 or more SampleMetadata.

    SampleMetadata objects provide a dataframe with a matching index to MSfileSet.

    A dataframe is created from a set of MS data files (MSfileSet) and joined with matching SampleMetadata.
    By default (metadata_inner_merge=False), all files in the passed MSfileSet will be included- even if no matching metadata is found.
    Passing metadata_inner_merge=True, will only include MS files that have matching metadata for every SampleMetadata included.

    SampleRun objects are created for each MS file when the SampleSet is created,
    but MS data is not initialized until called.
    """

    @log_timer
    def __init__(self, ms_file_set, *sample_metadata, metadata_inner_merge=False, init_ms=False):
        self._ms_file_set = ms_file_set
        self._metadata_tuple = sample_metadata

        self._df = self._ms_file_set.df

        # Create a dataframe of sample files paired with sample metadata
        for metadata in self._metadata_tuple:
            if metadata_inner_merge:
                self._df = pd.concat([self._df, metadata.df], axis=1, join='inner')
            else:
                self._df = pd.merge(self._df, metadata.df, how='left', left_index=True, right_index=True)

        # Create SampleRuns for the samples in the set
        self._create_sampleruns()

        # Apply metadata to SampleRuns for samples in the set with metadata
        for metadata in self._metadata_tuple:
            self._df.apply(lambda row: self._set_run_metadata(row.name, row['run'], metadata), axis=1)

        if init_ms:
            self.init_all_ms()

    def __repr__(self):
        return self.df.to_string()

    @staticmethod
    def _set_run_metadata(sample_name, run, metadata):
        """Adds metadata to SampleRuns, if possible.

        Samples with missing metadata are logged.
        """

        try:
            run._metadata = pd.concat([run._metadata, metadata.df.loc[sample_name]])

        # Log missing metadata for any MS file
        except KeyError:
            dir_path, file = os.path.split(metadata.file_path)
            logger.warning(f"Missing metadata from: {file}, for MS file: {sample_name}")

    def _create_sampleruns(self):
        """Creates of SampleRuns for all samples in the SampleSet.

        Multi or single process according to MP_SUPPORT.
        """

        if msAI.MP_SUPPORT:
            self._create_sampleruns_mp()
        else:
            self._create_sampleruns_sp()

    @log_timer
    def _create_sampleruns_sp(self):
        """Single-process creation of SampleRuns for all samples in the SampleSet."""

        self._df['run'] = self._df.apply(lambda row: SampleRun(row['path']), axis=1)

    @staticmethod
    def _create_samplerun_mpf(row):
        """Multiprocessing function to create a single SampleRun for a row/sample in the SampleSet."""

        row['run'] = SampleRun(row['path'])
        return row

    @log_timer
    def _create_sampleruns_mp(self):
        """Multiprocess creation of SampleRuns for all samples in the SampleSet."""

        self._df = MultiTaskDF.parallelize_on_rows(self._df, self._create_samplerun_mpf)

    @log_timer
    def _init_all_ms_sp(self):
        """Single-process initialization of MS data for all samples in the SampleSet."""

        self._df['run'].apply(SampleRun.init_ms)

    @staticmethod
    def _init_ms_mpf(row):
        """Multiprocessing function to initialize the MS data of a single SampleRun (a row of a SampleSet)."""

        row['run'].init_ms()
        return row

    @log_timer
    def _init_all_ms_mp(self):
        """Multiprocess initialization of MS data for all samples in the SampleSet."""

        self._df = MultiTaskDF.parallelize_on_rows(self._df, self._init_ms_mpf)

    @log_timer
    def _save_all_ms_sp(self, dir_path):
        """Single-process save of MS data for all samples in the SampleSet."""

        self._df['msAIr_hash'] = self._df.apply(lambda row: row['run'].save(dir_path, row.name), axis=1)

    @staticmethod
    def _save_ms_mpf(dir_path, row):
        """Multiprocessing function to save the MS data of a single SampleRun (a row of a SampleSet)."""

        row['msAIr_hash'] = row['run'].save(dir_path, row.name)
        return row

    @log_timer
    def _save_all_ms_mp(self, dir_path):
        """Multiprocess save of MS data for all samples in the SampleSet."""

        self._df = MultiTaskDF.parallelize_on_rows(self._df, partial(self._save_ms_mpf, dir_path))

    @property
    def df(self):
        """Get a dataframe of sample runs paired with sample metadata.

        Index: name (from filename)
        Columns: type, size_MB, path, (metadata...), run (python object)
        """

        return self._df

    def init_all_ms(self):
        """Initializes MS data for all samples in the SampleSet.

        Multi or single process according to MP_SUPPORT.
        """

        if msAI.MP_SUPPORT:
            self._init_all_ms_mp()
        else:
            self._init_all_ms_sp()

    def save_all_ms(self, dir_path):
        """Saves MS data for all samples in the set as .msAIr files (in dir_path) and add hash value to metadata (msAIr_hash).

        Multi or single process according to MP_SUPPORT.
        """

        if msAI.MP_SUPPORT:
            self._save_all_ms_mp(dir_path)
        else:
            self._save_all_ms_sp(dir_path)

    def save_metadata(self, dir_path, filename):
        """Saves all metadata for a SampleSet as a .msAIm file.

        This enables faster loading when recreating a sample set,
        and verification of msAIr_hash values.

        Contents will include all metadata passed at SampleSet creation + msAIr hash values (if created).
        MSfile data and SampleRuns are not included, as data paths may change.

        Data is serialized with pickle and compressed via bzip2.
        A sha256 hash is returned.
        """

        metadata = self._df.drop(columns=['file_type', 'file_size', 'path', 'run'])

        full_filename = (dir_path + "/" + filename + ".msAIm")
        msAIm_hash = Saver.save_obj(metadata, full_filename)

        return msAIm_hash


class SampleRun:
    """Holds data from a MS analysis run of a sample and any additional metadata.

    A `SampleRun` instance is created with a path reference that is used to create a future `MSfile`,
    or load MS data from a previously saved `SampleRun`.
    This allows a cheep view of this data to exist without importing it all into memory.
    A very large number of `SampleRun` instances can be created and their MS data initialized when needed.

    Typically, `SampleRun` instances are not manually created, but instead arise from a `SampleSet`.

    Data is extracted from a supported MS file type or loaded from a previous msAIr save.
    File type is determined by file extension (.mzML .msAIr).
    A sha256 hash may be provided for a .msAIr file which will be verified during init_ms().
    """

    file_path: str
    """A string representation of the path to the MS file."""

    _ms: msData.MSfile = None
    """MS data from a`.MSfile` or a msAIr save."""

    _metadata: Series = None
    """The metadata as a `.Series`."""

    def __init__(self, file_path):
        """Initializes an instance of SampleRun class.

        Args:
            file_path: A string representation of the path to the MS file.
                Path can be relative or absolute.

        """
        self.file_path = file_path

        # self._ms = msData.MSfile()
        # self._metadata = None

    @property
    def ms(self):
        """Access to MS data of a sample run."""

        return self._ms

    @property
    def metadata(self):
        """Access to sample metadata."""

        return self._metadata

    @property
    def msAIr_hash(self):
        """Hash value of the SampleRun.

        This value was generated when the SampleRun was saved,
        and re-associated from SampleSet metadata.
        """

        if hasattr(self._metadata, 'msAIr_hash'):
            return self._metadata.msAIr_hash
        else:
            return None

    def save(self, dir_path, filename):
        """Save a SampleRun ms data as a msAIr file for fast loading later.

        Data is serialized with pickle and compressed via bzip2.
        A sha256 hash is returned.
        """

        full_filename = (dir_path + "/" + filename + ".msAIr")
        msAIr_hash = Saver.save_obj(self._ms, full_filename)

        return msAIr_hash

    def init_ms(self):
        """Initialize MS data at the SampleRun's set file_path from a .mzML or .msAIr file.

        For a .msAIr file, it is first tested against a sha256 hash, if provided.
        Data is decompressed via bzip2 and deserialized with pickle.
        """

        name, ext = os.path.splitext(self.file_path)

        if ext.casefold() == '.mzml':
            ms_data = msData.MZMLfile(self.file_path)
            self._ms = ms_data

        elif ext.casefold() == '.msair':
            ms_data, hash_result = Saver.load_obj(self.file_path, self.msAIr_hash)
            self._ms = ms_data

            if hash_result is None:
                logger.info(f"No hash value for file: {self.file_path}")

            elif hash_result is False:
                logger.warning(f"Hash verification failed for file: {self.file_path}")

        else:
            raise SampleRunMSinitError(f"Invalid file type/extension: {self.file_path}")
