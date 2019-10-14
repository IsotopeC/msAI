
""""
test_msData

* Unit tests for msData
* See config for configuration

"""


from tests import config
from tests.fixtures import MSfile_interface, MZMLfile, spectrum, peak

import pytest


class TestMSfile:
    def test_MSfile_interface_exists(self, MSfile_interface):

        assert MSfile_interface

    @pytest.mark.parametrize("expected_attribute", config.MSfile_attributes)
    def test_MSfile_attribute_exists(self, MSfile_interface, expected_attribute):

        assert hasattr(MSfile_interface, expected_attribute)

    @pytest.mark.parametrize("expected_property", config.MSfile_properties)
    def test_MSfile_property_exists(self, MSfile_interface, expected_property):

        assert hasattr(MSfile_interface, expected_property)


class TestMZMLfile:
    def test_MZMLfile_exists(self, MZMLfile):

        assert MZMLfile

    @pytest.mark.parametrize("expected_attribute", config.MSfile_attributes)
    def test_MZMLfile_attribute_exists(self, MZMLfile, expected_attribute):

        assert hasattr(MZMLfile, expected_attribute)

    @pytest.mark.parametrize("expected_property", config.MSfile_properties)
    def test_MZMLfile_property_exists(self, MZMLfile, expected_property):

        assert hasattr(MZMLfile, expected_property)

    @pytest.mark.parametrize("MZMLfile_test_property", config.MSfile_test_properties)
    def test_MZMLfile_property_value(self, MZMLfile, MZMLfile_test_property):
        evaluated_value = getattr(MZMLfile, MZMLfile_test_property)
        key_value = getattr(MZMLfile.key, MZMLfile_test_property)

        assert evaluated_value == key_value


class TestSpectrum:
    def test_spectrum_exists(self, request, spectrum):
        ms_run = getattr(request.module, spectrum.run_id)
        evaluated_spectrum = ms_run.spectra.loc[spectrum.spec_id]

        assert evaluated_spectrum.any()

    @pytest.mark.parametrize("spectrum_test_value_name", config.MSfile_spectrum_values)
    def test_spectrum_value(self, request, spectrum, spectrum_test_value_name):
        ms_run = getattr(request.module, spectrum.run_id)
        evaluated_spectrum = ms_run.spectra.loc[spectrum.spec_id]

        evaluated_value = getattr(evaluated_spectrum, spectrum_test_value_name)
        key_value = getattr(spectrum, spectrum_test_value_name)

        assert evaluated_value == key_value


class TestPeak:
    def test_peak_exists(self, request, peak):
        ms_run = getattr(request.module, peak.run_id)
        evaluated_peak = ms_run.peaks.loc[peak.spec_id, peak.peak_number]

        assert evaluated_peak.any()

    @pytest.mark.parametrize("peak_test_value_name", config.MSfile_peak_values)
    def test_peak_value(self, request, peak, peak_test_value_name):
        ms_run = getattr(request.module, peak.run_id)
        evaluated_peak = ms_run.peaks.loc[peak.spec_id, peak.peak_number]

        evaluated_value = getattr(evaluated_peak, peak_test_value_name)
        key_value = getattr(peak, peak_test_value_name)

        assert evaluated_value == key_value

