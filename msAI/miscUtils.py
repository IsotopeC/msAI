
"""Miscellaneous utilities used by msAI.

"""


import msAI
from msAI.errors import MiscUtilsError

import logging
import sys
import os
import platform
import itertools
import hashlib
import pickle
import bz2
import multiprocessing
from multiprocessing import Pool
from functools import partial
import pathlib

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)
"""Module logger."""


class FileGrabber:
    """Functions to grab files."""

    @staticmethod
    def multi_extensions(directory, *extensions, recursive=True):
        """Returns an iterator of path objects to all files in a directory matching the passed extensions.

        Extensions are specified without leading ``.``.
        Use str(path_obj) to get the platform independent path string.
        Subdirectories will be recursively searched by default.

        Note:
            While Windows paths are case insensitve, Posix paths are case sensitive.
            Thus the set of casefolded extensions will be used on Windows systems.
        """

        dir_path = pathlib.Path(directory)
        path_type = FileGrabber.path_type(directory)

        ext_list = list(set(extensions))
        if path_type == 'windows':
            ext_list = list(set(map(str.casefold, ext_list)))

        # Add glob pattern to extensions
        ext_list = list(map("".join, zip(*[(["*."] * len(ext_list))] + [ext_list])))

        if recursive:
            glob_func = dir_path.rglob
        else:
            glob_func = dir_path.glob

        return itertools.chain.from_iterable(glob_func(pattern) for pattern in ext_list)

    @staticmethod
    def path_type(directory='.'):
        """Get the path type of a directory.

        Returns a string of either 'posix' or 'windows'.
        Path type is identified by the class of Path object created.

        This test is used for determining what glob patterns to apply based on path case sensitivity.
        Windows paths are case insensitve, while Posix paths are case sensitive.
        """

        path = pathlib.Path(directory)

        if isinstance(path, pathlib.PosixPath):
            return 'posix'

        elif isinstance(path, pathlib.WindowsPath):
            return 'windows'

        else:
            raise MiscUtilsError("Unknown path type")


class Sizer:
    """Functions to measure data size."""

    @staticmethod
    def obj_mb(obj):
        """Returns the size of a python object in MBs."""

        obj_size_mb = (sys.getsizeof(obj) * 0.000001)
        return obj_size_mb

    @staticmethod
    def print_obj_mb(obj):
        """Prints the size of a python object in MBs."""

        obj_size_mb = Sizer.obj_mb(obj)
        print(f"objSizeMB: {obj_size_mb:.4f}")

    @staticmethod
    def file_mb(file):
        """Returns the size of a file in MBs."""

        obj_size_mb = (os.path.getsize(file) * 0.000001)
        return obj_size_mb

    @staticmethod
    def print_file_mb(file):
        """Prints the size of a file in MBs, to 4 decimals."""

        file_size_mb = Sizer.file_mb(file)
        print(f"fileSizeMB: {file_size_mb:.4f}")


class Saver:
    """Functions to save / load, serialize, and compress files and objects."""

    @staticmethod
    def save_obj(obj, file):
        """Saves a python object to the path/filename given.

        Data is serialized with pickle and compressed via bzip2.
        A sha256 hash is returned.
        """

        file_path = pathlib.Path(file)
        with bz2.open(file_path, "wb") as save_file:
            pickle.dump(obj, save_file, pickle.HIGHEST_PROTOCOL)

        return Saver.get_hash(file_path)

    @staticmethod
    def get_hash(file):
        """Calculate the sha256 hash of a file."""

        # The size of each read from the file
        BLOCK_SIZE = 65536

        file_hash = hashlib.sha256()

        with open(file, 'rb') as file:
            file_block = file.read(BLOCK_SIZE)
            while len(file_block) > 0:
                file_hash.update(file_block)
                file_block = file.read(BLOCK_SIZE)

        # Return the hexadecimal digest of the hash
        return file_hash.hexdigest()

    @staticmethod
    def verify_hash(file, test_hash):
        """Verifies the sha256 hash of a file."""

        calc_hash = Saver.get_hash(file)

        if calc_hash == test_hash:
            return True
        else:
            return False

    @staticmethod
    def load_obj(file, check_hash=None):
        """Loads a previously saved object at the given path/filename.

        The file will be tested against a sha256 hash, if provided.
        Data is decompressed via bzip2 and deserialized with pickle.

        The object is returned along with results of verify_hash, or none if no hash is present.
        """

        if check_hash is not None:
            if Saver.verify_hash(file, check_hash):
                hash_verified = True
            else:
                hash_verified = False
        else:
            hash_verified = None

        with bz2.open(file, "rb") as file:
            obj = pickle.load(file)

        return obj, hash_verified


class MultiTaskDF:
    """Use multiprocessing to parallelize a function applied to all rows in a dataframe."""

    @staticmethod
    def _parallelize(df_in, func):
        """Partition a dataframe and assign a pool of workers to apply a function to each part.

        Splits a dataframe into a number of subsets equal to cpu count,
        and creates a process pool with a number of workers equal to cpu count,
        and use each worker to apply a function to a dataframe subset.

        ``func`` is received as a partial object, and its call input is completed with
        a dataframe subset after the dataframe is split.
        """

        worker_count = msAI.WORKER_COUNT
        df_split = np.array_split(df_in, worker_count)
        pool = Pool(worker_count)

        with pool:
            df_out = pd.concat(pool.map(func, df_split), sort=False)

        return df_out

    @staticmethod
    def _run_on_subset(func, df_subset):
        """Applies a function to a dataframe subset."""

        return df_subset.apply(func, axis=1)

    @staticmethod
    def parallelize_on_rows(df, func):
        """Parallelizes a function applied to all rows in a dataframe."""

        return MultiTaskDF._parallelize(df, partial(MultiTaskDF._run_on_subset, func))


class EnvInfo:
    """Functions to get info about the environment running python."""

    @staticmethod
    def platform():
        """Get a string (multiline) describing the platform in use."""

        return (f"Platform: {sys.platform}\n"
                f"Full Platform: {platform.platform()}\n"
                f"Machine Type: {platform.machine()}\n"
                f"Network Name: {platform.node()}")

    @staticmethod
    def os():
        """Get a string (multiline) describing the operating system in use."""

        def env_item_gen():
            """Generator to iterate over key-value pairs of environment variables."""

            for key, value in os.environ.items():
                yield (f"{key}: {value}")

        return (f"OS Type: {os.name}\n"
                f"OS Path Type: {FileGrabber.path_type()}\n"
                f"Multiprocessing Method: {multiprocessing.get_start_method()}\n"
                f"OS Environment Variables:\n    {(os.linesep + '    ').join(env_item_gen())}")

    @staticmethod
    def python():
        """Get a string (multiline) describing the python interpreter in use."""

        return (f"Python Version: {platform.python_version()}\n"
                f"Python Implementation: {platform.python_implementation()}\n"
                f"Interpreter Compiler: {platform.python_compiler()}\n"
                f"Python Executable Path: {sys.executable}\n"
                f"Python Command Line Arguments:\n    {(os.linesep + '    ').join(sys.argv)}\n"
                f"Python Path:\n    {(os.linesep + '    ').join(sys.path)}")

    @staticmethod
    def all():
        """Get a string (multiline) describing the environment running python."""

        return os.linesep.join([EnvInfo.platform(), EnvInfo.os(), EnvInfo.python()])

    @staticmethod
    def mp_method():
        """Get a string describing the start method used by the multiprocessing module to create new processes.

        Defaults are set according to OS type:
            | POSIX = 'fork'
            | Windows = 'spawn'

        Use this function to test and switch to single processing if necessary.
        Certain functions will fail under the spawn start method.
        """

        return multiprocessing.get_start_method()
