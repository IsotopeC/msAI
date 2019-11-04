
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

>>> sample1_ms = msData.MZMLfile(sample1_mzml_path)

The `.MSfile` interface provides several properties for accessing MS metadata.

>>> sample1_ms.run_id
'EP2421'

>>> sample1_ms.run_date
'2017-06-28T04:10:21Z'

>>> sample1_ms.ms_file_version
'1.1.0'

>>> sample1_ms.spectrum_count
651

>>> sample1_ms.peak_count
1430013

>>> sample1_ms.tic_sum
103151911964.0

MS data is structured in dataframes and
accessed by the `~.MSfile.spectra` and `~.MSfile.peaks` properties.

Spectra dataframe structure
    | **Index:**  spec_id
    | **Columns:**  rt,  peak_count,  tic,  ms_lvl,  filters

>>> sample1_ms.spectra
             rt  peak_count           tic  ms_lvl                                    filters
299    3.018841        1745  4.697734e+07       1  FTMS + p ESI Full ms [115.0000-1000.0000]
301    3.039366        1836  4.806605e+07       1  FTMS + p ESI Full ms [115.0000-1000.0000]
303    3.060012        2060  4.775426e+07       1  FTMS + p ESI Full ms [115.0000-1000.0000]
305    3.080646        1828  4.685581e+07       1  FTMS + p ESI Full ms [115.0000-1000.0000]
307    3.101156        1847  4.875970e+07       1  FTMS + p ESI Full ms [115.0000-1000.0000]

Peaks dataframe structure
    | **First Index Level:**  spec_id
    | **Second Index Level:**  peak_number
    | **Columns:**  rt,  mz,  i

>>> sample1_ms.peaks
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


Get an individual spectrum with spec_id value.

>>> sample1_ms.spectra.loc[303]
rt                                              3.06001
peak_count                                         2060
tic                                         4.77543e+07
ms_lvl                                                1
filters       FTMS + p ESI Full ms [115.0000-1000.0000]
Name: 303, dtype: object

Get a summary / distribution of peak values.

>>> sample1_ms.peaks.describe().round(2)
               rt          mz             i
count  1430013.00  1430013.00  1.430013e+06
mean         9.83      283.99  7.123009e+04
std          3.71      160.93  1.726981e+06
min          3.02      115.00  8.504700e+02
25%          6.79      167.07  5.720040e+03
50%          9.93      229.14  1.181848e+04
75%         12.90      349.25  3.166049e+04
max         16.00      999.95  9.182814e+08

Get all peaks in a spectrum with spec_id value.

>>> sample1_ms.peaks.loc[303]
                   rt         mz             i
peak_number
0            3.060012  115.03925  41569.882812
1            3.060012  115.05054   2562.014648
2            3.060012  115.07562   1966.861328
3            3.060012  115.08680   2180.555420
4            3.060012  115.52079   1273.498047
               ...        ...           ...
2055         3.060012  717.65051   2805.519287
2056         3.060012  787.67346   2972.889648
2057         3.060012  896.67566   2859.390381
2058         3.060012  909.33502   3785.186035
2059         3.060012  926.53265   2564.230713
[2060 rows x 3 columns]

Get a single peak with spec_id and peak_number.

>>> sample1_ms.peaks.loc[303, 100]
rt        3.060012
mz      125.060060
i     10957.689453
Name: (303, 100), dtype: float64


Creating a set of MS files from a data directory
------------------------------------------------

Define the data directory path.
By default, contents of sub directories will be recursively included.

>>> mzml_dir = "./examples/data/mzML"

Create a set of the MS files in the data directory.
This set is structured as a dataframe.
Creating a `.MSfileSet` does not import the MS data into memory.
Rather, it provides a quick view of the MS data files available for use.
The next *Sample Sets* example demonstrates how this MS file set is used to create a `.SampleSet`
and access the underlying MS data.


>>> ms_files = msData.MSfileSet(mzml_dir)
>>> ms_files
         file_type  file_size                            path
filename
EP0482        mzML  12.862821  examples/data/mzML/EP0482.mzML
EP2421        mzML  15.133800  examples/data/mzML/EP2421.mzML
EP2536        mzML  12.745723  examples/data/mzML/EP2536.mzML


Adding additional sample metadata
=================================

*(in progress)*
