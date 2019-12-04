
"""Miscellaneous utilities used by msAI.

Todo
    * Add type info for funcs passed as arguments

"""


import msAI
from msAI.errors import MiscUtilsError
from msAI.types import DF

import logging
import sys
import os
import platform
import itertools
from typing import Iterable, Optional, Tuple
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
    def multi_extensions(directory: str,
                         *extensions: str,
                         recursive: bool = True) -> Iterable[pathlib.Path]:
        """Creates an iterator of path objects to all files in a directory matching the passed extensions.

        Use ``str(path_obj)`` to get the platform independent path string.
        Subdirectories will be recursively searched by default.

        Args:
            directory: A string representation of the path to the directory.
                Path can be relative or absolute.
            extensions: One or more file extensions specified as strings without leading (.).
            recursive: A boolean indicating if files in subdirectories are included.
                Defaults to `True`.

        Returns:
             An iterator of path objects to all files found.
        """

        dir_path = pathlib.Path(directory)
        path_type = FileGrabber.path_type(directory)
        ext_list = list(set(extensions))

        # While Windows paths are case insensitive, Posix paths are case sensitive.
        # Thus the set of casefolded extensions will be used on Windows systems.
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
    def path_type(directory: str = '.') -> str:
        """Get the path type of a directory.

        Path type is identified by the class of Path object created.
        This test is used for determining what glob patterns to apply based on path case sensitivity.
        Windows paths are case insensitive, while Posix paths are case sensitive.

        Args:
            directory: A string representation of the path to the directory.
                Path can be relative or absolute. Defaults to current directory.

        Returns:
            A string of either `'posix'` or `'windows'`, indicating the path type.

        Raises:
            MiscUtilsError: For unknown path type.
        """

        path = pathlib.Path(directory)

        if isinstance(path, pathlib.PosixPath):
            return 'posix'

        elif isinstance(path, pathlib.WindowsPath):
            return 'windows'

        else:
            raise MiscUtilsError("Unknown path type")


class Sizer:
    """Functions to measure memory / storage sizes."""

    @staticmethod
    def obj_mb(obj: object) -> float:
        """Measures the memory size of a python object in MBs.

        Args:
            obj: The python object to measure.

        Returns:
            The Python object's size in memory in MBs.
        """

        obj_size_mb = (sys.getsizeof(obj) * 0.000001)
        return obj_size_mb

    @staticmethod
    def print_obj_mb(obj: object):
        """Prints the memory size of a python object in MBs to 4 decimals.

        Args:
            obj: The python object to measure.
        """

        obj_size_mb = Sizer.obj_mb(obj)
        print(f"objSizeMB: {obj_size_mb:.4f}")

    @staticmethod
    def file_mb(file: str):
        """Measures the storage size of a file in MBs.

        Args:
            file: A string representation of the path to the file to measure.
                Path can be relative or absolute.

        Returns:
            The storage size of the file in MBs.
        """

        file_size_mb = (os.path.getsize(file) * 0.000001)
        return file_size_mb

    @staticmethod
    def print_file_mb(file: str):
        """Prints the storage size of a file in MBs to 4 decimals.

        Args:
            file: A string representation of the path to the file to measure.
                Path can be relative or absolute.
        """

        file_size_mb = Sizer.file_mb(file)
        print(f"fileSizeMB: {file_size_mb:.4f}")


class Saver:
    """Functions to save / load, serialize, and compress files and objects."""

    @staticmethod
    def save_obj(obj: object,
                 file: str) -> str:
        """Saves a python object to the path / filename given.

        Data is serialized with pickle and compressed via bzip2.
        A sha256 hash is also calculated.

        Args:
            obj: The python object to save.
            file: A string representation of the path to the file to save.
                Path can be relative or absolute.

        Returns:
            A sha256 hash as a string.
        """

        file_path = pathlib.Path(file)
        with bz2.open(file_path, "wb") as save_file:
            pickle.dump(obj, save_file, pickle.HIGHEST_PROTOCOL)

        return Saver.get_hash(file)

    @staticmethod
    def get_hash(file: str) -> str:
        """Calculates the sha256 hash of a file.

        Args:
            file: A string representation of the path to the file to calculate a hash for.
                Path can be relative or absolute.

        Returns:
            A sha256 hash as a string.
        """

        # The size of each read from the file
        block_size = 65536

        file_hash = hashlib.sha256()

        file_path = pathlib.Path(file)
        with open(file_path, 'rb') as file:
            file_block = file.read(block_size)
            while len(file_block) > 0:
                file_hash.update(file_block)
                file_block = file.read(block_size)

        # Return the hexadecimal digest of the hash
        return file_hash.hexdigest()

    @staticmethod
    def verify_hash(file: str,
                    test_hash: str) -> bool:
        """Verifies the sha256 hash of a file.

        Args:
            file: A string representation of the path to the file to calculate and compare hash value for.
                Path can be relative or absolute.
            test_hash: A sha256 hash as a string to test against.

        Returns:
            A boolean indicating if the hash value is verified.
            `True` means the calculated hash matches the test hash.
        """

        calc_hash = Saver.get_hash(file)

        if calc_hash == test_hash:
            return True
        else:
            return False

    @staticmethod
    def load_obj(file: str,
                 test_hash: Optional[str] = None) -> Tuple[object, Optional[bool]]:
        """Loads a previously saved object.

        The file will be tested against a sha256 hash, if provided.
        Data is decompressed via bzip2 and deserialized with pickle.

        Args:
            file: A string representation of the path to the file to load the object from.
                Path can be relative or absolute.
            test_hash: A sha256 hash as a string to test against.

        Returns:
            A tuple of the object and an optional boolean indicating if the hash of the saved file was verified.
        """

        if test_hash is not None:
            if Saver.verify_hash(file, test_hash):
                hash_verified = True
            else:
                hash_verified = False
        else:
            hash_verified = None

        file_path = pathlib.Path(file)
        with bz2.open(file_path, "rb") as file:
            obj = pickle.load(file)

        return obj, hash_verified


class MultiTaskDF:
    """Functions to parallelize work on dataframes through multiprocessing."""

    @staticmethod
    def _partition_by_rows(df_in: DF,
                           subset_func) -> DF:
        """Partitions a dataframe into subsets across rows and assigns a worker to each to apply a function.

        Creates a process pool with a number of workers equal to cpu count (by default),
        and splits the dataframe `df_in` into a number of subsets equal to number of workers.
        Each worker applies the `subset_func` to a dataframe subset in parallel.

        Args:
            df_in: The input dataframe.
            subset_func: A partial object containing the function to apply to each dataframe subset.
                This is received as a partial object, and its call input is completed with
                a dataframe subset after the dataframe is split.

        Returns: A dataframe formed by concating all subset results.
        """

        worker_count = msAI.WORKER_COUNT
        df_part = np.array_split(df_in, worker_count)
        pool = Pool(worker_count)

        with pool:
            df_out = pd.concat(pool.map(subset_func, df_part), sort=False)

        return df_out

    @staticmethod
    def _run_on_subset_rows(func,
                            df_subset: DF) -> DF:
        """Applies a function to each row in a dataframe subset.

        Rows are passed to `func` as `Series` objects whose index is the dataframe's columns.

        Args:
            func: The function to apply to each row in the `df_subset`.
                This function must be a static method and return the row, reflecting the results.
                Additional arguments can be passed with a partial object by the caller.
            df_subset: A dataframe subset, to which a single worker applies `func` to all rows.

        Returns: A dataframe reflecting the changes from the applied `func`.
        """

        return df_subset.apply(func, axis=1)

    @staticmethod
    def parallelize_on_rows(df: DF,
                            func) -> DF:
        """Applies a function to rows in a dataframe in parallel.

        Args:
            df: The input dataframe.
            func: The function to apply to each row in the `df`.
                This function must be a static method and return the row, reflecting the results.
                Additional arguments can be passed with a partial object by the caller.

        Returns: A new dataframe reflecting the changes from the applied `func`.
        """

        return MultiTaskDF._partition_by_rows(df, partial(MultiTaskDF._run_on_subset_rows, func))


class EnvInfo:
    """Functions to get info about the environment running python."""

    @staticmethod
    def platform() -> str:
        """Get a string (multiline) describing the platform in use."""

        return (f"Platform: {sys.platform}\n"
                f"Full Platform: {platform.platform()}\n"
                f"Machine Type: {platform.machine()}\n"
                f"Network Name: {platform.node()}")

    @staticmethod
    def os() -> str:
        """Get a string (multiline) describing the operating system in use."""

        def env_item_gen():
            """Generator to iterate over key-value pairs of environment variables."""

            for key, value in os.environ.items():
                yield f"{key}: {value}"

        return (f"OS Type: {os.name}\n"
                f"OS Path Type: {FileGrabber.path_type()}\n"
                f"Multiprocessing Method: {multiprocessing.get_start_method()}\n"
                f"OS Environment Variables:\n    {(os.linesep + '    ').join(env_item_gen())}")

    @staticmethod
    def python() -> str:
        """Get a string (multiline) describing the python interpreter in use."""

        return (f"Python Version: {platform.python_version()}\n"
                f"Python Implementation: {platform.python_implementation()}\n"
                f"Interpreter Compiler: {platform.python_compiler()}\n"
                f"Python Executable Path: {sys.executable}\n"
                f"Python Command Line Arguments:\n    {(os.linesep + '    ').join(sys.argv)}\n"
                f"Python Path:\n    {(os.linesep + '    ').join(sys.path)}")

    @staticmethod
    def all() -> str:
        """Get a string (multiline) describing the environment running python."""

        return os.linesep.join([EnvInfo.platform(), EnvInfo.os(), EnvInfo.python()])

    @staticmethod
    def mp_method() -> str:
        """Get a string describing the start method used by the multiprocessing module to create new processes.

        Defaults are set according to OS type:
            | POSIX = 'fork'
            | Windows = 'spawn'

        Use this function to test and switch to single processing if necessary.
        Certain functions will fail under the spawn start method.
        """

        return multiprocessing.get_start_method()
