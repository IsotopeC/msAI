
"""msAI module for importing mass spectrometry data into dataframes.

Features
    * Extraction of data from MS files (mzML, TBD...)
    * Creation of in-memory data structures for spectra / peaks values
    * Building a set of MS data files

Todo
    * Change MSfile to dataclass
    * Change properties to attributes
    * Modify public / private
    * Create types for peaks and spectra dataframes

"""


import msAI.miscUtils as miscUtils
from msAI.errors import MSfileSetInitError
from msAI.miscDecos import log_timer

import os
import logging
from typing import ClassVar, List

import pandas as pd
import pymzml


logger = logging.getLogger(__name__)
"""Module logger."""


class MSfile:
    """Interface class for accessing data from a MS file stored in various file types.

    Subclass implementations provide support for the various file types
    and override the init method to set values.
    The `peaks` and `spectra` properties hold data structured in dataframes.
    """

    def __init__(self):
        self._run_id = None
        self._run_date = None
        self._ms_file_version = None

        self._spectrum_count = None
        self._peak_count = None
        self._tic_sum = None

        self._peaks = pd.DataFrame()
        self._spectra = pd.DataFrame()

    @property
    def run_id(self):
        """Get the sample's run ID as specified from its MS data file."""

        return self._run_id

    @property
    def run_date(self):
        """Get the date the sample was run as specified from its MS data file."""

        return self._run_date

    @property
    def ms_file_version(self):
        """Get the data format version in which the sample was originally saved as specified from its ms file.

        Note: Currently, this is equivalent to mzML version number.
        """

        return self._ms_file_version

    @property
    def spectrum_count(self):
        """Get the number of MS spectra from a sample run.

        This value is calculated from the number of spectra imported, rather than from MS file metadata.
        """

        return self._spectrum_count

    @property
    def peak_count(self):
        """Get the total number of MS peaks from all MS spectra in sample run."""

        return self._peak_count

    @property
    def tic_sum(self):
        """
        Get the total ion current sum of all spectra in sample run
        """

        return self._tic_sum

    @property
    def peaks(self):
        """Get a dataframe of all peaks in a MS file.

        Dataframe structure
            | **First Index Level:**  spec_id
            | **Second Index Level:**  peak_number
            | **Columns:**  rt,  mz,  i
        """

        return self._peaks

    @property
    def spectra(self):
        """Get a dataframe of all spectra in an MS file.

        Dataframe structure
            | **Index:**  spec_id
            | **Columns:**  rt,  peak_count,  tic,  ms_lvl,  filters
        """

        return self._spectra


class MZMLfile(MSfile):
    """Class to access MS data stored in an mzML file."""

    def __init__(self,
                 mzml_file_path: str):
        """Initializes an instance of MZMLfile class.

        Args:
            mzml_file_path: A string representation of the path to the mzML data file.
                Path can be relative or absolute.
        """
        self._mzml_file_path = mzml_file_path
        self._run = pymzml.run.Reader(self._mzml_file_path)

        # self._peaks = pd.DataFrame()
        # self._spectra = pd.DataFrame()
        self._create_dfs()

        self._run_id = self._run.info['run_id']
        # self.spectrum_count = self._run.info['spectrum_count']
        self._run_date = self._run.info['start_time']
        self._ms_file_version = self._run.info['mzml_version']

        self._spectrum_count = self.spectra.index.size
        self._tic_sum = self.spectra['tic'].sum()       # Total number of MS peaks from all spectra
        self._peak_count = self.peaks.index.size        # Total ion current sum of all spectra

        del self._run

    def _create_spectrum_peaks_df(self, spectrum):
        """Creates a dataframe of all the peaks for a single spectrum in an mzML file."""

        mz_values = spectrum.mz.round(5)
        i_values = spectrum.i
        rt = spectrum.scan_time_in_minutes()
        peak_count = len(mz_values)
        spectrum_id = [spectrum.ID]
        peak_list = list(range(peak_count))

        peak_index = pd.MultiIndex.from_product([spectrum_id, peak_list], names=['spec_id', 'peak_number'])
        peaks = {'rt': rt,
                 'mz': mz_values,
                 'i': i_values}
        spectrum_peaks = pd.DataFrame(peaks, index=peak_index)

        return spectrum_peaks

    def _create_spectrum_df(self, spectrum):
        """Creates a dataframe of all the spectra in an mzML file."""

        rt = spectrum.scan_time_in_minutes()
        peak_count = len(spectrum.mz)
        tic = spectrum.TIC
        ms_lvl = spectrum.ms_level
        filters = spectrum.get('filter string')
        spectrum_id = [spectrum.ID]

        spec = {'rt': rt,
                'peak_count': peak_count,
                'tic': tic,
                'ms_lvl': ms_lvl,
                'filters': filters}
        spectrum_df = pd.DataFrame(spec, index=spectrum_id)

        return spectrum_df

    def _create_dfs(self):
        """Creates spectra and peaks dataframes for an mzML file.

        This method sets the following properties:
            * self._peaks
            * self._spectra
        """

        peaks_df_list = []
        spectra_df_list = []

        for n, spectrum in enumerate(self._run):
            spectrum_peaks_df = self._create_spectrum_peaks_df(spectrum)
            peaks_df_list.append(spectrum_peaks_df)

            spectrum_df = self._create_spectrum_df(spectrum)
            spectra_df_list.append(spectrum_df)

        self._peaks = pd.concat(peaks_df_list)
        self._spectra = pd.concat(spectra_df_list)


class MSfileSet:
    """Class to create a set of MS files from a data directory.

    Creating a set enables a large number of datafiles to be viewed / manipulated as a dataframe,
    without loading their entire contents into memory.

    By default, contents of sub directories will be recursively included.
    However, an error is raised if included filenames are duplicated.
    A Set can include any MSfile type (mzML, msAIr, or a mix).
    By default, any datafile matching these extensions will be included.
    An exclusive type may alternatively be specified.
    """

    mzML_exts: ClassVar[List[str]] = ['mzML', 'mzml', 'MZML']
    """File extensions considered to be mzML files."""

    msAIr_exts: ClassVar[List[str]] = ['msAIr', 'msair', 'MSAIR']
    """File extensions considered to be msAIr files."""
    
    @log_timer
    def __init__(self,
                 dir_path: str,
                 data_type: str = 'all',
                 recursive: bool = True):
        """Initializes an instance of MSfileSet class.

        Args:
            dir_path: A string representation of the path to the data directory.
                Path can be relative or absolute.
            data_type: (``'all'``, ``'mzML'``, ``'msAIr'``) The type of MS files to include in the set.
                By default, all types are included.
            recursive: A boolean indicating if files in subdirectories are included in the set.
                Defaults to ``True``.

        Raises:
            MSfileSetInitError: For duplicated filenames.
        """

        self._dir_path = dir_path

        if data_type == 'all':
            ext_list = self.mzML_exts + self.msAIr_exts
        elif data_type == 'mzML':
            ext_list = self.mzML_exts
        elif data_type == 'msAIr':
            ext_list = self.msAIr_exts
        else:
            raise MSfileSetInitError(f"Invalid data_type: {data_type}")

        if recursive:
            self._file_iter = miscUtils.FileGrabber.multi_extensions(self._dir_path, *ext_list)
        else:
            self._file_iter = miscUtils.FileGrabber.multi_extensions(self._dir_path, *ext_list, recursive=False)

        def file_gen():
            for datafile in self._file_iter:
                file_size = miscUtils.Sizer.file_mb(datafile)

                path_head, path_tail = os.path.split(datafile)
                filename, file_ext = os.path.splitext(path_tail)

                # Fix mixed cases extensions to have same file_type value
                if file_ext.replace(".", "").casefold() == 'mzml':
                    file_type = 'mzML'
                elif file_ext.replace(".", "").casefold() == 'msair':
                    file_type = 'msAIr'

                yield (filename, file_type, file_size, str(datafile))

        # Initial import into a dataframe with integer index
        self._hf = pd.DataFrame(file_gen(), columns=['filename', 'file_type', 'file_size', 'path'])

        # Test if any filenames are duplicated
        duplicates = self._hf[self._hf.duplicated('filename', keep=False)]
        if duplicates.size > 0:
            raise MSfileSetInitError(f"Duplicated filenames:\n {duplicates.to_string()}")

        else:
            self._df = self._hf.set_index('filename', verify_integrity=True)

    def __repr__(self):
        return self._df.to_string()

    @property
    def df(self):
        """Get a dataframe of MS files.

        Dataframe structure
            | **Index:**  name (from filename)
            | **Columns:**  type,  size_MB,  path
        """
        return self._df
