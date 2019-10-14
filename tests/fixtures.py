
""""
fixtures

* Reusable fixtures for use by test functions

"""


import msAI.msData as msData
from tests import key

import pytest


def get_spectrum_test_id(spectrum):
    id_string = str(spectrum.run_id) + ":spec" + str(spectrum.spec_id)
    return id_string


def get_peak_test_id(peak):
    id_string = str(peak.run_id) + ":spec" + str(peak.spec_id) + ":peak" + str(peak.peak_number)
    return id_string


@pytest.fixture()
def MSfile_interface():
    return msData.MSfile()


@pytest.fixture(scope="module", params=key.mzml_files_list)
def MZMLfile(request):
    mzml_test_file = msData.MZMLfile(request.param)

    # Add answer key containing the correct values tests should return
    mzml_test_file.key = getattr(key, mzml_test_file.run_id + '_key')

    # Assign to a variable equal to run_id for individual reference later without recreation
    setattr(request.module, mzml_test_file.run_id, mzml_test_file)

    return mzml_test_file


@pytest.fixture(params=key.spectrum_list, ids=get_spectrum_test_id)
def spectrum(request):
    return request.param


@pytest.fixture(params=key.peak_list, ids=get_peak_test_id)
def peak(request):
    return request.param

