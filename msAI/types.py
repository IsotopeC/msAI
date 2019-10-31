
"""Module containing types used by msAI.

"""


from typing import NewType
import logging

import pandas as pd


logger: logging.Logger = logging.getLogger(__name__)
"""Module logger."""

# Series = pd.Series
# """Type alias of a Pandas Series."""

Series: NewType = NewType("Series", pd.Series)
"""Type derived from Pandas Series."""

DF = pd.DataFrame
"""Type alias of a Pandas DataFrame."""

MetaDF = NewType("MetaDF", DF)
"""Type derived from `DF` for use with metadata."""
