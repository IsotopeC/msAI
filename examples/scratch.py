
"""
msAI demo

Demonstration of sample set creation from metadata and MS data files

"""


# Import msAI modules
import msAI.msData as msData
from msAI.samples import SampleSet
from msAI.metadata import SampleMetadata

import pandas as pd
import pymzml
import sys
import os
import resource

print(resource.getrlimit(resource.RLIMIT_AS))
resource.setrlimit(resource.RLIMIT_AS, (1073741824, -1))
print(resource.getrlimit(resource.RLIMIT_AS))


# Set pandas to display all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Paths to example data directories
mzml_dir = "./examples/data/mzML"
msAIr_dir = "./examples/data/msAIr"
msAIm_dir = "./examples/data/msAIm"

# Paths to example data files
csv_path = "./examples/data/metadata/coneflower_metadata.csv"
# sample1_mzml_path = "./examples/data/mzML/EP2421.mzML"
sample1_mzml_path = "./examples/data/mzML/brukerEx1.mzML"
sample_set1_msAIm_path = "./examples/data/msAIm/sample_set1.msAIm"


# metadata
# --------------------------------------------------------------------------------

# Import sample metadata from a CSV file and attempt to set an index
#   * Contents initially imported into a dataframe with a numerical index
#   * Metadata labels and values are analyzed and a new index is assigned, if possible
#   * This index is used to match metadata with sample file
cone_flower_metadata = SampleMetadata(csv_path)

# Access the dataframe with the 'df' attribute
cone_flower_metadata.df

# Get a summary of metadata contents
cone_flower_metadata.describe()

# Manually set the dataframe index from an existing dataframe column
#   (Unless it is not suitable for use as an index)
# cone_flower_metadata.set_index('new_index')

# Import more metadata- multiple metadata files can be used
# more_metadata = SampleMetadata(more_meta_path)


# msData
# --------------------------------------------------------------------------------

# Create set of MS files from a data directory
ms_files = msData.MSfileSet(mzml_dir)
ms_files

# By default, contents of sub directories will be recursively included
#   * Can also specify file type
# less_ms_files = msData.MSfileSet(mzml_dir, data_type='mzML', recursive=False)

# Creating an MSfileSet does not import MS data
#   * Rather, it provides an summary of what is available
#   * Cheep to create for large datasets


# Reader Interface
# ================================================================================
# The Reader class selectively extracts data from an mzML file and exposes the data as a python object
# The reader itself is an iterator, thus looping over all spectra follows the classical python syntax
# Spectra can also be accessed by their nativeID

# Initialize Reader object for a given mzML file
s1run = pymzml.run.Reader(sample1_mzml_path)

# Get the number of spectra in file
s1run.get_spectrum_count()

# Get the next spectrum element as an object via iterator
s1run.next()
# = <__main__.Spectrum object with native ID 299 at 0x7fd0818b06a0>


# Run Info
# --------------------------------------------------------------------------------
for key, value in s1run.info.items():
    print(f"{key}: {value}")


# Spectrum IDs and Attributes
# --------------------------------------------------------------------------------
# Get a spectrum from a run by native ID
spec331 = s1run[331]

# Get the native ID of a spectrum
spec331.ID

# Get the index of the spectrum
#   This does not necessarily correspond to the native spectrum ID
spec331.index

# Get the ms_level
spec331.ms_level

# Get the retention time and retention time unit of a spectrum
spec331.scan_time

# Get the retention time retention time in minutes of a spectrum
spec331.scan_time_in_minutes()

# Get the total ion current for a spectrum
spec331.TIC

# Get minimum and maximum m/z value of a spectrum
spec331.extreme_values("mz")

# Get minimum and maximum intensity value of a spectrum
spec331.extreme_values("i")


# Accession / OBO Values
# --------------------------------------------------------------------------------
# Get a dict of all entries stored the id attribute of a spectrum
spec331.id_dict

spec331.get("scan window lower limit")

spec331.get("scan window upper limit")

spec331.get("ms level")


# Whole Spectrum Values
# --------------------------------------------------------------------------------
# Get peaks as an array of mz/i lists (or a list of mz/i tuples if reprofiled)
#   Supported types are: raw, centroided and reprofiled
#   If data is already centroided, raw = centroided
spec331.peaks('centroided')

spec331.peaks('raw').shape


def obj_mb(obj):
    """
    Return the size of a python object in MBs
    """
    obj_size_mb = (sys.getsizeof(obj) * 0.000001)
    return obj_size_mb


def spectrum_peak_count(spectrum):
    """
    Return the total number of centroided peaks in a spectrum
    """
    total_peaks = len(spectrum.peaks('centroided'))
    return total_peaks


def spectrum_peak_array_mb(spectrum):
    """
    Return the size in MB of the array used to store all centroided peaks for a spectrum
    """
    total_mb = obj_mb(spectrum.peaks('centroided'))
    return total_mb


def print_all_spectra_info(mzml_file):
    """
    Print summary info for each spectrum in an mzML file and cumulative totals
    """
    run = pymzml.run.Reader(mzml_file)
    total_peaks = 0
    total_mb = 0
    for n, spec in enumerate(run):
        spec_peaks = spectrum_peak_count(spec)
        spec_mb = spectrum_peak_array_mb(spec)
        total_peaks += spec_peaks
        total_mb += spec_mb
        print(f"SpecID {spec.ID:5}",
              f"@ RT {spec.scan_time_in_minutes():5.2f} |",
              f"MS lvl {spec.ms_level},",
              f"Filters: {spec.get('filter string')} |",
              f"Peak Count: {spec_peaks:5} |",
              f"Mem: {spec_mb:4.3f} MB")
    print(f"Parsed {run.get_spectrum_count()} spectra from {mzml_file} |",
          f"Total Peak Count: {total_peaks} |",
          f"Total Mem: {total_mb:.3f} MB")


# print_all_spectra_info(sample1_mzml_path)


def _create_spectrum_df(spectrum):
    """Creates a dataframe of all the spectra in an mzML file."""

    rt = spectrum.scan_time_in_minutes()
    peak_count = len(spectrum.mz)

    try:
        tic = spectrum.TIC
    except AttributeError:
        tic = None

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

specDF = _create_spectrum_df(spec331)
specDF


def _create_spectrum_peaks_df(spectrum):
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


specDFpeaks = _create_spectrum_peaks_df(spec331)
specDFpeaks

# MS data is accessed using a MSfile interface

# Import MS data from mzML file
sample1_ms = msData.MZMLfile(sample1_mzml_path)

# Access MS metadata
sample1_ms.run_id
sample1_ms.run_date
sample1_ms.ms_file_version
sample1_ms.spectrum_count
sample1_ms.peak_count
sample1_ms.tic_sum

# The 'peaks' and 'spectra' properties hold dataframes

# Spectra
#   * Index: spec_id
#   * Columns: rt, peak_count, tic, ms_lvl, filters
sample1_ms.spectra

# Get an individual spectrum with spec_id value
sample1_ms.spectra.loc[303]

# Peaks
#   * First Index Level: spec_id
#   * Second Index Level: peak_number
#   * Columns: rt, mz, i
sample1_ms.peaks

# Summary / distribution of peak values
sample1_ms.peaks.describe()

# Get all peaks in a spectrum with spec_id value
sample1_ms.peaks.loc[303]

# Get a single peak with spec_id and peak_number
sample1_ms.peaks.loc[303, 100]


# samples
# --------------------------------------------------------------------------------
# Instead of creating a MSfile interface for each data file,
#   * SampleSet provides a dataframe of SampleRuns
#   * Created from a MSfileSet and paired with 0 or more SampleMetadata

# By default, all files in the MSfileSet will be included- even if no matching metadata is found
#   * Passing metadata_inner_merge=True, will only include MS files that have matching metadata

# SampleRun objects are created for each MS file when the SampleSet is created
#   * MS data is not initialized until called
#   * Provides a quick view of what is available

# Create a SampleSet- Pairing MS data with sample metadata, default is to join on index of MS files
#
sample_set = SampleSet(ms_files, cone_flower_metadata)
sample_set

# Get a single sample with filename
sample_set.df.loc["EP2421"]

# Get metadata values with label names
sample_set.df.loc["EP2421"].plantID
sample_set.df.loc["EP2421"].tissue
sample_set.df.loc["EP2421"].site
sample_set.df.loc["EP2421"].treatment

# Note that SampleRuns are created
sample_set.df.loc["EP2421"].run
# But MS data is not available until initialized
# sample_set.df.loc["EP2421"].run.ms.spectra

# Initialize MS data
sample_set.init_all_ms()

# Access MS data and metadata
sample_set.df.loc["EP2421"].run.ms.run_date

spectra = sample_set.df.loc["EP2421"].run.ms.spectra
spectra

peaks = sample_set.df.loc["EP2421"].run.ms.peaks
peaks

# Access select spectra (rows) based on their column values)
spectra = sample_set.df.loc["EP2421"].run.ms.spectra
# by rt
spectra.loc[spectra['rt'] > 12]
# by ms_lvl
ms1 = spectra.loc[spectra['ms_lvl'] == 1]
ms1
# Get only ms1 peaks
peaks = sample_set.df.loc["EP2421"].run.ms.peaks
peaks.loc[ms1.index]


# Saving / Loading
# --------------------------------------------------------------------------------

# Save initialized samples via by serializing and compressing
#   * Faster access later (do not need to parse mzML files)
#   * Smaller storage size
#   * Any calculations / manipulations are also saved

# Save all samples in set as .msAIr files to a directory
#   * Same filenames are used
sample_set.save_all_ms(msAIr_dir)

# A hash value is added to metadata
sample_set.df['msAIr_hash']

# Save SampleSet metadata as a .msAIm file to a directory
sample_set.save_metadata(msAIm_dir, "sample_set1")


# Reload previously saved msAIr data

# Define a MSfileSet of the .msAIr files
#   * .msAIr and .mzML files can be defined in same MSfileSet
msAIr_set = msData.MSfileSet(msAIr_dir)
msAIr_set
# Compare to the mzML version
ms_files

# Define SampleMetadata from a .msAIm file
msAIm = SampleMetadata(sample_set1_msAIm_path)
msAIm

# Define SampleSet and initialize
sample_set1 = SampleSet(msAIr_set, msAIm)
sample_set1.init_all_ms()
sample_set1

# Access same as before
sample_set1.df.loc["EP2421"]
sample_set1.df.loc["EP2421"].plantID
sample_set1.df.loc["EP2421"].tissue
sample_set1.df.loc["EP2421"].site
sample_set1.df.loc["EP2421"].treatment
sample_set1.df.loc["EP2421"].run.ms.run_date
sample_set1.df.loc["EP2421"].run.ms.spectra
sample_set1.df.loc["EP2421"].run.ms.peaks

