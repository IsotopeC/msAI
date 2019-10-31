
"""msAI module for importing sample metadata into dataframes.

Features
    * Extraction of metadata from various file types
    * Importing metadata into a dataframe
    * Verification of metadata usability
    * Auto indexing of metadata

Todo
    * Move .msAIm saving to this module
    * Refactor auto indexing
    * Add anomaly detection
    * Add additional file types: TBD...

"""


from msAI.errors import MetadataVerifyError, MetadataIndexError, MetadataInitError
from msAI.types import Series, DF, MetaDF
from msAI.miscUtils import Saver
from msAI.miscDecos import log_timer

import os
import logging

import pandas as pd


logger: logging.Logger = logging.getLogger(__name__)
"""Module logger."""


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

    file_path: str
    """A string representation of the path to the metadata file."""

    _hf: DF
    """High fidelity copy of imported data.
    
    Leave this original data untouched for future reference if needed.
    """

    df: MetaDF
    """The metadata dataframe."""

    @log_timer
    def __init__(self,
                 file_path: str,
                 auto_index: bool = True):
        """Initializes an instance of SampleMetadata class.

        Args:
            file_path: A string representation of the path to the metadata file.
                Path can be relative or absolute.
            auto_index: A boolean indicating if the metadata should be automatically indexed.
                Default is True.

        Raises:
            MetadataInitError: For an invalid file type/extension.
        """

        self.file_path = file_path

        name, ext = os.path.splitext(self.file_path)

        # CSV import
        if ext.casefold() == ".csv":
            self._hf = pd.read_csv(self.file_path)

            self.df = self._hf.copy()

            # Verify imported metadata is usable
            self._verify_import()

            if auto_index:
                # Assign an index, if possible
                self._auto_index()

        # msAIm import
        elif ext.casefold() == ".msaim":
            metadata, hash_result = Saver.load_obj(self.file_path)
            self.df = metadata

        else:
            raise MetadataInitError(f"Invalid file type/extension: {self.file_path}")

    def __repr__(self):
        """Returns a string representation of the metadata dataframe."""

        return self.df.to_string()

    def _verify_import(self):
        """Verifies the imported metadata is usable.

        Ensures at least one metadata entry/row and
        at least two metadata labels/columns exist.

        Raises:
            MetadataVerifyError: If No metadata entries or not enough metadata labels are found
        """

        def verify_entries_count():
            # Ensure at least one metadata entry/row exists
            row_count = self.df.shape[0]
            if row_count < 1:
                raise MetadataVerifyError("No metadata entries found")

        def verify_label_count():
            # Ensure at least two metadata labels/columns exist
            column_count = self.df.columns.size
            if column_count < 2:
                raise MetadataVerifyError(f"Not enough metadata labels: {column_count} labels found")

        verify_entries_count()
        verify_label_count()

    def _auto_index(self):
        """Attempts to identify and set the dataframe index from a metadata label/column.

        This index is used to match metadata to `.SampleRun`.
        """

        def most_unique_label() -> Series:
            """Gets the label(s)/column(s) with the most unique values - a possible index.

            More than one label will be returned if there are ties.

            Returns:
                A series of count value index by label name
            """

            return self.df.nunique().nlargest(1, keep='all')

        def verify_index(possible_index):
            """Ensures contents of imported metadata is suitable for auto indexing."""

            def verify_unique_label_values():
                """Ensures a label/column has a unique value for all entries/rows."""

                row_count = self.df.shape[0]
                unique_col_value_count = possible_index[0]

                if row_count != unique_col_value_count:
                    raise MetadataIndexError(f"Count of unique metadata labels (n={unique_col_value_count}) not equal to entry count (n={row_count})")

            def verify_single_unique_label():
                """Ensures a only a single label/column has a unique value for all entries/rows.

                Otherwise, more than one label is suitable for use as index- the user must decide.
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
            self.df.set_index(index_name, inplace=True, verify_integrity=True)

    def describe(self):
        """Prints a summary of metadata contents."""

        print(self.df.describe().to_string())

    def set_index(self,
                  new_index: str):
        """Manually sets the metadata dataframe index to an existing label/column.

        This index is used to match metadata to `.SampleRun`.

        Args:
            new_index: The name of the metadata label/column to use as the index.
        """

        self.df.set_index(new_index, inplace=True, verify_integrity=True)
