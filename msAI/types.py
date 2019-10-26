
"""Module containing types used by msAI.

"""


from typing import NewType
import logging

import pandas as pd


logger: logging.Logger = logging.getLogger(__name__)
"""Module logger configured with this module's name."""

Series = pd.Series
"""Type alias of a Pandas Series."""

DF = pd.DataFrame
"""Type alias of a pandas DataFrame."""

MetaDF: NewType = NewType("MetaDF",  DF)
"""Type derived from DF for use with metadata."""
