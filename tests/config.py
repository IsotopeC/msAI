
""""
config

* Update variables used by unit tests as msAI evolves

"""


import pytest
from collections import namedtuple


# Attributes that should exist in the MSfile interface and have values provided by subclass implementations (mzMLfile)
MSfile_attributes = ['_run_id',
                     '_run_date',
                     '_ms_file_version',
                     '_spectrum_count',
                     '_peak_count',
                     '_tic_sum',
                     '_peaks',
                     '_spectra']

# Add a failing test for an attribute
# MSfile_fail_test_attribute = pytest.param("_stuff", marks=pytest.mark.xfail(strict=True))
# MSfile_attributes.append(MSfile_fail_test_attribute)


# Properties that should exist in the MSfile interface and have values provided by subclass implementations (mzMLfile)
MSfile_properties = ['run_id',
                     'run_date',
                     'ms_file_version',
                     'spectrum_count',
                     'peak_count',
                     'tic_sum',
                     'peaks',
                     'spectra']

# Add a failing test for a property
# MSfile_fail_test_property = pytest.param("stuff", marks=pytest.mark.xfail(strict=True))
# MSfile_properties.append(MSfile_fail_test_property)


# Properties to value test (omits peaks and spectra, which are value tested later)
MSfile_test_properties = ['run_id',
                          'run_date',
                          'ms_file_version',
                          'spectrum_count',
                          'peak_count',
                          'tic_sum']

MSfile_spectrum_values = ['rt',
                          'peak_count',
                          'tic',
                          'ms_lvl',
                          'filters']

MSfile_peak_values = ['rt',
                      'mz',
                      'i']

TestMSspectrum = namedtuple('TestMSpectrum', ['run_id',
                                              'spec_id',
                                              'rt',
                                              'peak_count',
                                              'tic',
                                              'ms_lvl',
                                              'filters'])

TestMSpeak = namedtuple('TestMSpeak', ['run_id',
                                       'spec_id',
                                       'peak_number',
                                       'rt',
                                       'mz',
                                       'i'])

MSfileKey = namedtuple('MSfileKey', MSfile_test_properties)

