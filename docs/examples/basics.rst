
***********
Basic Usage
***********


Working with mass spectrometry data files
=========================================

Accessing data from a MS sample run
-----------------------------------

Define the path to a MS data file, in this case a mzML file type.

>>> sample1_mzml_path = "./examples/data/mzML/EP2421.mzML"

MS data is accessed using a `.MSfile` implementation matching the file type.
`.MZMLfile` is used with mzML files. On creation, the mzML file is imported into memory.

>> sample1_ms = msData.MZMLfile(sample1_mzml_path)

The `.MSfile` interface provides several properties for accessing MS metadata.

>>> sample1_ms.run_id
>>> sample1_ms.run_date
>>> sample1_ms.ms_file_version
>>> sample1_ms.spectrum_count
>>> sample1_ms.peak_count
>>> sample1_ms.tic_sum

MS data is structured in dataframes and
accessed by the `.MSfile.spectra` and `.MSfile.peaks` properties.

Spectra dataframe structure
    | **Index:**  spec_id
    | **Columns:**  rt,  peak_count,  tic,  ms_lvl,  filters

print(sample1_ms.spectra.to_string()[:2000])


Peaks dataframe structure
    | **First Index Level:**  spec_id
    | **Second Index Level:**  peak_number
    | **Columns:**  rt,  mz,  i

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




Create set of MS files from a data directory
--------------------------------------------

Define the data directory path.
By default, contents of sub directories will be recursively included.

>>> mzml_dir = "./examples/data/mzML"

Create a set of the MS files in the data directory.
This set is structured as a dataframe.
Creating a `.MSfileSet` does not import the MS data into memory.
Rather, it provides a quick view of the MS data files available for use.
The next *Samples* example demonstrates how this MS file set is used to create a `.SampleSet`
and access the underlying MS data.


>>> ms_files = msData.MSfileSet(mzml_dir)
>>> ms_files
         file_type  file_size                            path
filename
EP0482        mzML  12.862821  examples/data/mzML/EP0482.mzML
EP2421        mzML  15.133800  examples/data/mzML/EP2421.mzML
EP2536        mzML  12.745723  examples/data/mzML/EP2536.mzML

