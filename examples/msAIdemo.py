
"""
msAI demo

Demonstration of sample set creation from metadata and MS data files

"""


# Import msAI modules
import msAI.msData as msData
from msAI.samples import SampleSet
from msAI.metadata import SampleMetadata


# Paths to example data directories
mzml_dir = "./examples/data/mzML"
msAIr_dir = "./examples/data/msAIr"
msAIm_dir = "./examples/data/msAIm"

# Paths to example data files
csv_path = "./examples/data/metadata/coneflower_metadata.csv"
sample1_mzml_path = "./examples/data/mzML/EP2421.mzML"
sample_set1_msAIm_path = "./examples/data/msAIm/sample_set1.msAIm"


# metadata
# --------------------------------------------------------------------------------

# Import sample metadata from a CSV file and attempt to set an index
#   * Contents initially imported into a dataframe with a numerical index
#   * Metadata labels and values are analyzed and a new index is assigned, if possible
#   * This index is used to match metadata with sample file
cone_flower_metadata = SampleMetadata(csv_path)
print(str(cone_flower_metadata)[:2000])

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
less_ms_files = msData.MSfileSet(mzml_dir, data_type='mzML', recursive=False)
less_ms_files

# Creating an MSfileSet does not import MS data
#   * Rather, it provides an summary of what is available
#   * Cheep to create for large datasets

# MS data is accessed using a MSfile interface

# Import MS data from mzML file
cf1_ms = msData.MZMLfile(sample1_mzml_path)

# Access MS metadata
cf1_ms.run_id
cf1_ms.run_date
cf1_ms.ms_file_version
cf1_ms.spectrum_count
cf1_ms.peak_count
cf1_ms.tic_sum

# The 'peaks' and 'spectra' properties hold dataframes

# Spectra
#   * Index: spec_id
#   * Columns: rt, peak_count, tic, ms_lvl, filters
print(cf1_ms.spectra.to_string()[:2000])

# Get an individual spectrum with spec_id value
cf1_ms.spectra.loc[303]

# Peaks
#   * First Index Level: spec_id
#   * Second Index Level: peak_number
#   * Columns: rt, mz, i
cf1_ms.peaks

# Summary / distribution of peak values
cf1_ms.peaks.describe()

# Get all peaks in a spectrum with spec_id value
cf1_ms.peaks.loc[303]

# Get a single peak with spec_id and peak_number
cf1_ms.peaks.loc[303, 100]


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

# Creat a SampleSet- Pairing MS data with sample metadata, default is to join on index of MS files
#
sample_set = SampleSet(ms_files, cone_flower_metadata)
sample_set

# Get a single sample with filename
sample_set.df.loc["EP2421"]

# Get get metadata values with label names
sample_set.df.loc["EP2421"].plantID
sample_set.df.loc["EP2421"].tissue
sample_set.df.loc["EP2421"].site
sample_set.df.loc["EP2421"].treatment

# Note that SampleRuns are created
sample_set.df.loc["EP2421"].run
# But MS data is not available until initialized
sample_set.df.loc["EP2421"].run.ms.spectra

# Initialize MS data
sample_set.init_all_ms()

# Access MS data and metadata
sample_set.df.loc["EP2421"].run.ms.run_date
sample_set.df.loc["EP2421"].run.ms.spectra
sample_set.df.loc["EP2421"].run.ms.peaks


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
cf_set = SampleSet(msAIr_set, msAIm)
cf_set.init_all_ms()
cf_set

# Access same as before
cf_set.df.loc["EP2421"]
cf_set.df.loc["EP2421"].plantID
cf_set.df.loc["EP2421"].tissue
cf_set.df.loc["EP2421"].site
cf_set.df.loc["EP2421"].treatment
cf_set.df.loc["EP2421"].run.ms.run_date
cf_set.df.loc["EP2421"].run.ms.spectra
cf_set.df.loc["EP2421"].run.ms.peaks

