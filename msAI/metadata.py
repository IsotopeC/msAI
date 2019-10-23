
"""Module for importing sample metadata into dataframes.

Features provided include
    * Extraction of metadata from various file types
    * Importing metadata into a dataframe
    * Verification of metadata usability
    * Auto indexing of metadata

Todo
    * Change properties to attributes
    * Move .msAIm saving to this module
    * Refactor auto indexing
    * Add anomaly detection
    * Add additional file types: TBD...

"""


from msAI.errors import MetadataVerifyError, MetadataIndexError, MetadataInitError
from msAI.miscUtils import Saver
from msAI.miscDecos import log_timer

import os
import logging

import pandas as pd


logger = logging.getLogger(__name__)


class SampleMetadata:
    """Imports sample metadata from a supported file type into a dataframe and assigns an index.

    Supported file types: *.csv*, *.msAIm*, TBD...
    (A *.msAIm* file can be created from a previous `.SampleSet`).

    Content from the metadata file is initially imported into a dataframe with a default numerical index.
    By default, metadata labels and values are analyzed and if possible, a new index is assigned from an existing column.
    This index is used by `.SampleSet` to match this metadata with corresponding MS data in `.MSfileSet`.

    Requirements to auto index metadata imported into a dataframe:
        * Dataframe has 1 or more rows
        * Dataframe has 2 or more columns
        * For one and only one column:

            * All column values are unique
            * All entries/rows have a value for this column
    """

    @log_timer
    def __init__(self,
                 file_path: str,
                 auto_index: bool = True):
        """
        Args:
            file_path: A string representation of the path to the metadata file.
                Path can be relative or absolute.
            auto_index (optional): A boolean indicating if the metadata should be automatically indexed.
                Default is True.

        Attributes:
            file_path (str): The string representation of the path to the metadata file.
            _hf (DataFrame): High fidelity copy of raw imported data.

        Raises:
            MetadataInitError: For an invalid file type/extension.
        """

        self.file_path: str = file_path

        name, ext = os.path.splitext(self.file_path)

        if ext.casefold() == ".csv":
            # High fidelity import (leave this raw/original data untouched for future reference if needed)
            self._hf = pd.read_csv(self.file_path)

            # Make a copy of data
            self._df = self._hf.copy()

            # Verify imported metadata is usable
            self._verify_import()

            if auto_index:
                # Assign an index, if possible
                self._auto_index()

        elif ext.casefold() == ".msaim":
            metadata, hash_result = Saver.load_obj(self.file_path)
            self._df = metadata

        else:
            raise MetadataInitError(f"Invalid file type/extension: {self.file_path}")

    def __repr__(self):
        """Returns a string representation of the metadata dataframe."""

        return self._df.to_string()

    @property
    def df(self):
        """The dataframe of the metadata."""

        return self._df

    def _verify_import(self):
        """Verifies the imported metadata is usable.

        Ensures at least one metadata entry/row and
        at least two metadata labels/columns exist.

        Raises:
            MetadataVerifyError: If No metadata entries or not enough metadata labels are found
        """

        def verify_entries_count():
            # Ensure at least one metadata entry/row exists
            row_count = self._df.shape[0]
            if row_count < 1:
                raise MetadataVerifyError("No metadata entries found")

        def verify_label_count():
            # Ensure at least two metadata labels/columns exist
            column_count = self._df.columns.size
            if column_count < 2:
                raise MetadataVerifyError(f"Not enough metadata labels: {column_count} labels found")

        verify_entries_count()
        verify_label_count()

    def _auto_index(self):
        """Attempts to identify and set the dataframe index from a metadata label/column.

        This index is used to match metadata to `.SampleRun`.
        """

        def most_unique_label():
            """
            Get the label(s)/column(s) with the most unique values - a possible index
                More than one label will be returned if there are ties

            Returns a series of count value index by label name
            """
            return self._df.nunique().nlargest(1, keep='all')

        def verify_index(possible_index):
            """
            Ensure contents of imported metadata is suitable for auto indexing
            """

            def verify_unique_label_values():
                """Ensure a label/column has a unique value for all entries/rows"""
                row_count = self._df.shape[0]
                unique_col_value_count = possible_index[0]

                if row_count != unique_col_value_count:
                    raise MetadataIndexError(f"Count of unique metadata labels (n={unique_col_value_count}) not equal to entry count (n={row_count})")

            def verify_single_unique_label():
                """
                Ensure a only a single label/column has a unique value for all entries/rows
                    Otherwise, more than one label is suitable for use as index- the user must decide
                """
                possible_index_count = possible_index.shape[0]

                if possible_index_count > 1:
                    raise MetadataIndexError(f"{possible_index_count} labels possible for use as index")

            verify_unique_label_values()
            verify_single_unique_label()

        possible_index_label = most_unique_label()

        try:
            verify_index(possible_index_label)
        except MetadataIndexError as err:
            logger.error(f"Can not auto index metadata: {err}")
        else:
            index_name = possible_index_label.index[0]
            self._df.set_index(index_name, inplace=True, verify_integrity=True)

    def describe(self):
        """Prints a summary of metadata contents."""

        print(self._df.describe().to_string())

    def set_index(self,
                  new_index: str):
        """Manually sets the metadata dataframe index to an existing label/column.

        This index is used to match metadata to `.SampleRun`.

        Args:
            new_index: The name of the metadata label/column to use as the index.
        """

        self._df.set_index(new_index, inplace=True, verify_integrity=True)
