
"""
Concurrency Benchmark

Workflow performing the following:
    * Importing metadata from CSV
    * Importing a data dir of 500 mzML files
    * Pairing MS data and sample metadata
    * Saving sample set via serialization and compressing (.msAIr)
    * Reloading saved samples, with hash verification

Results (2x E5-2690 CPUs, 192 GB RAM)
    Run times:
        * Multiprocess (32 workers) = 9 min (9.4x)
        * Single-process = 85 min

    Data sizes:
        * 500 mzML files = 6.9 GB
        * 500 msAIr files = 4.3 GB (37.7% less)

    Reload times:
        * msAIr saves 2.5 mins reloading 500 samples with mp (2.9x faster)
        * msAIr saves 28.3 mins reloading 500 samples without mp (4.2x faster)
"""


import msAI.msData as msData
from msAI.samples import SampleSet
from msAI.metadata import SampleMetadata


# Paths to data and metadata
mzml_dir = "/home/c/MSdata/bm/32mzml"
msAIr_dir = "/home/c/MSdata/bm/msAIr"
msAIm_dir = "/home/c/MSdata/bm/msAIm"
meta_path = "/home/c/MSdata/bm/metadata.csv"
msAIm_path = "/home/c/MSdata/bm/msAIm/sample_set_1.msAIm"

# Import metadata and attempt to set index
sample_metadata = SampleMetadata(meta_path)

# Recursively grab all MS files
ms_files = msData.MSfileSet(mzml_dir)

# Pair MS data with sample metadata, default is to join on file index
sample_set = SampleSet(ms_files, sample_metadata)

# Initialize MS data
sample_set.init_all_ms()

# Save via by serializing and compressing, for fast access later
sample_set.save_all_ms(msAIr_dir)

# Save SampleSet metadata
sample_set.save_metadata(msAIm_dir, "sample_set_1")

# Reload previously saved msAIr data
msAIr_set = msData.MSfileSet(msAIr_dir)
msAIm = SampleMetadata(msAIm_path)
sample_set_msAI = SampleSet(msAIr_set, msAIm)

# Initialize msAIrs
sample_set_msAI.init_all_ms()


