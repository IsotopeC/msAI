
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

Create the `.SampleSet`.

>>> sample_set = SampleSet(ms_files, cone_flower_metadata)
>>> sample_set
         file_type  file_size                            path   class sampleType       site block treatment plantID  tissue     siteblock   sitetreatment polarity                                                run
filename
EP0482        mzML  12.862821  examples/data/mzML/EP0482.mzML  sample     sample  Rosemount    B1      HIGH    P360    seed  Rosemount_B1  Rosemount_HIGH  unknown  <msAI.samples.SampleRun object at 0x7f063ff54f50>
EP2421        mzML  15.133800  examples/data/mzML/EP2421.mzML  sample     sample  Rosemount    B1        R1    P109  flower  Rosemount_B1    Rosemount_R1  unknown  <msAI.samples.SampleRun object at 0x7f063fed80d0>
EP2536        mzML  12.745723  examples/data/mzML/EP2536.mzML  sample     sample  Rosemount    B1       LOW    P134    root  Rosemount_B1   Rosemount_LOW  unknown  <msAI.samples.SampleRun object at 0x7f063ff35550>


Accessing sample MS data and metadata
=====================================

*(in progress)*


Saving and loading sample sets
==============================

*(in progress)*
