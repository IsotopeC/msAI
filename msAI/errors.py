
"""
errors

* Definition of msAI exceptions

"""


import logging


logger = logging.getLogger(__name__)


class Error(Exception):
    """
    Base class for exceptions in this module
    """
    pass


class RootError(Error):
    """
    Exceptions raised for errors in msAI package __init__

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class MiscUtilsError(Error):
    """
    Exceptions raised for errors in miscUtils

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class MetadataError(Error):
    """
    Exceptions raised for errors in metadata

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class MetadataInitError(MetadataError):
    """
    Exceptions raised for errors in initializing metadata

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class MetadataVerifyError(MetadataError):
    """
    Exceptions raised for errors in verifying imported metadata

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class MetadataIndexError(MetadataError):
    """
    Exceptions raised for errors in setting metadata index

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class SampleRunError(Error):
    """
    Exceptions raised for errors in SampleRun

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class SampleRunMSinitError(SampleRunError):
    """
    Exceptions raised for errors in initializing MS data in SampleRun

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class MSdataError(Error):
    """
    Exceptions raised for errors in msData

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class MSfileSetInitError(MSdataError):
    """
    Exceptions raised for errors in initializing MSfileSet

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
