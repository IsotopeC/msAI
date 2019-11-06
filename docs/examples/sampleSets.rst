
***********
Sample Sets
***********

This example demonstrates how to define an entire sample set
which will automatically create a `.MSfile` interface for each data file.
This demo uses the `.MSfileSet` and `.SampleMetadata` from the previous :doc:`example <basics>`
to create a `.SampleSet`.


Creating a sample set
=====================

Create the `.MSfileSet` instance.

>>> mzml_dir = "./examples/data/mzML"
>>> ms_files = msData.MSfileSet(mzml_dir)

Create the `.SampleMetadata` instance.

>>> csv_path = "./examples/data/metadata/coneflower_metadata.csv"
>>> cone_flower_metadata = SampleMetadata(csv_path)

Create the `.SampleSet`. A set can be constructed from any `.MSfileSet` along with 0 or more `.SampleMetadata`.
Upon creation, `.SampleRun` instances are created for each MS file, but the MS data will not initialized until called.
This allows a cheep view of the entire set to exist without importing all the data into memory.

>>> sample_set = SampleSet(ms_files, cone_flower_metadata)
>>> sample_set
         file_type  file_size                            path   class sampleType       site block treatment plantID  tissue     siteblock   sitetreatment polarity                                                run
filename
EP0482        mzML  12.862821  examples/data/mzML/EP0482.mzML  sample     sample  Rosemount    B1      HIGH    P360    seed  Rosemount_B1  Rosemount_HIGH  unknown  <msAI.samples.SampleRun object at 0x7f063ff54f50>
EP2421        mzML  15.133800  examples/data/mzML/EP2421.mzML  sample     sample  Rosemount    B1        R1    P109  flower  Rosemount_B1    Rosemount_R1  unknown  <msAI.samples.SampleRun object at 0x7f063fed80d0>
EP2536        mzML  12.745723  examples/data/mzML/EP2536.mzML  sample     sample  Rosemount    B1       LOW    P134    root  Rosemount_B1   Rosemount_LOW  unknown  <msAI.samples.SampleRun object at 0x7f063ff35550>


Accessing sample MS data and metadata
=====================================

Get a single sample with filename.

>>> sample_set.df.loc["EP2421"]
file_type                                                     mzML
file_size                                                  15.1338
path                                examples/data/mzML/EP2421.mzML
class                                                       sample
sampleType                                                  sample
site                                                     Rosemount
block                                                           B1
treatment                                                       R1
plantID                                                       P109
tissue                                                      flower
siteblock                                             Rosemount_B1
sitetreatment                                         Rosemount_R1
polarity                                                   unknown
run              <msAI.samples.SampleRun object at 0x7f063fed80d0>
Name: EP2421, dtype: object


Get metadata values with label names.

>>> sample_set.df.loc["EP2421"].plantID
'P109'

>>> sample_set.df.loc["EP2421"].tissue
'flower'

>>> sample_set.df.loc["EP2421"].site
'Rosemount'

>>> sample_set.df.loc["EP2421"].treatment
'R1'


Note that a `.SampleRun` is created,

>>> sample_set.df.loc["EP2421"].run
<msAI.samples.SampleRun object at 0x7f063fed80d0>

But MS data is not available until initialized.

>>> sample_set.df.loc["EP2421"].run.ms.spectra
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "/home/c/Repos/msAI/msAI/samples.py", line 252, in ms
    return self._ms
AttributeError: 'SampleRun' object has no attribute '_ms'

Initialize all MS data.

>>> sample_set.init_all_ms()


Access MS data and metadata.

>>> sample_set.df.loc["EP2421"].run.ms.run_date
'2017-06-28T04:10:21Z'

>>> sample_set.df.loc["EP2421"].run.ms.spectra
             rt  peak_count          tic  ms_lvl                                    filters
299    3.018841        1745   46977344.0       1  FTMS + p ESI Full ms [115.0000-1000.0000]
301    3.039366        1836   48066048.0       1  FTMS + p ESI Full ms [115.0000-1000.0000]
303    3.060012        2060   47754260.0       1  FTMS + p ESI Full ms [115.0000-1000.0000]
305    3.080646        1828   46855808.0       1  FTMS + p ESI Full ms [115.0000-1000.0000]
307    3.101156        1847   48759696.0       1  FTMS + p ESI Full ms [115.0000-1000.0000]
         ...         ...          ...     ...                                        ...
1591  15.918533        3416  118047380.0       1  FTMS + p ESI Full ms [115.0000-1000.0000]
1593  15.938479        3328  128021860.0       1  FTMS + p ESI Full ms [115.0000-1000.0000]
1595  15.958450        3348  128402500.0       1  FTMS + p ESI Full ms [115.0000-1000.0000]
1597  15.978360        3156  152132620.0       1  FTMS + p ESI Full ms [115.0000-1000.0000]
1599  15.998312        3285  174533700.0       1  FTMS + p ESI Full ms [115.0000-1000.0000]
[651 rows x 5 columns]

>>> sample_set.df.loc["EP2421"].run.ms.peaks
                            rt         mz             i
spec_id peak_number
299     0             3.018841  115.03919  36447.125000
        1             3.018841  115.05045   2975.487549
        2             3.018841  115.07568   2015.634644
        3             3.018841  115.51699   1233.632690
        4             3.018841  115.96244   4875.453613
                        ...        ...           ...
1599    3280         15.998312  987.60944  12299.823242
        3281         15.998312  989.54504  39011.988281
        3282         15.998312  991.56219  57488.519531
        3283         15.998312  992.56891  21931.212891
        3284         15.998312  993.56921   7275.180176
[1430013 rows x 3 columns]


Saving and loading sample sets
==============================

In this example workflow so far, the step requiring the most computational resources / time to complete is when the
MS data is initialized - where data stored in mzML files is loaded into memory and structured as dataframes.
When working with large datasets, this step becomes expensive to repeat.
If samples will be needed again, they can be saved in an alternative format (msAIr file) that enables faster access and smaller storage size.
This msAIr file type is created by serializing and compressing
a `.SampleRun` instance, saving the state of all its in-memory data attributes.
While there is a upfront cost to creating a msAIr save, a `.SampleRun` is loaded from a msAIr file
much faster as it is not necessary to parse the mzML file again.
Additionally, since the entire `.SampleRun` instance is saved, the result of any calculations performed or new
data attributes created will also be saved.

Saving
------

Define the paths to the directories where data will be saved.

>>> msAIr_dir = "./examples/data/msAIr"
>>> msAIm_dir = "./examples/data/msAIm"

Save all the samples in the `.SampleSet` as msAIr files to a directory.
The same filenames are used with the ``.msAIr`` extension.

>>> sample_set.save_all_ms(msAIr_dir)

A hash value is calculated for each sample and added to the `.SampleSet` metadata.

>>> sample_set.df['msAIr_hash']

Save the `.SampleSet` metadata as a msAIm file to a directory.

>>> sample_set.save_metadata(msAIm_dir, "sample_set1")


