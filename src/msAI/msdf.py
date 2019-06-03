
import sys
import pickle
import bz2
import numpy as np
import pandas as pd
import pymzml


# Various functions for creating and evaluating in-memory data structures from MS data

def obj_mb(obj):
    """
    Return the size of a python object in MBs
    """
    obj_size_mb = (sys.getsizeof(obj) * 0.000001)
    return obj_size_mb


def print_obj_mb(obj):
    """
    Print the size of a python object in MBs
    """
    obj_size_mb = obj_mb(obj)
    print(f"objSizeMB: {obj_size_mb:.4f}")


def print_mzml_info(mzml_file):
    """
    Print info for an mzML file
    """
    run = pymzml.run.Reader(mzml_file)
    for key, value in run.info.items():
        print(f"{key}: {value}")


def print_all_spectra_info(mzml_file):
    """
    Print summary info for each spectrum in an mzML file and cumulative totals
    """
    run = pymzml.run.Reader(mzml_file)
    total_peaks = 0
    total_mb = 0
    total_tic = 0
    for n, spec in enumerate(run):
        spec_tic = spec.TIC
        spec_peaks = spectrum_peak_count(spec)
        spec_mb = spectrum_peak_array_mb(spec)
        total_tic += spec_tic
        total_peaks += spec_peaks
        total_mb += spec_mb
        print(f"SpecID {spec.ID:5}",
              f"@ RT {spec.scan_time_in_minutes():5.2f} |",
              f"MS lvl {spec.ms_level},",
              f"Filters: {spec.get('filter string')} |",
              f"TIC: {spec_tic:10.0f} |",
              f"Peak Count: {spec_peaks:5} |",
              f"Mem: {spec_mb:4.3f} MB")
    print(f"Parsed {run.get_spectrum_count()} spectra from {mzml_file} |",
          f"TIC: {total_tic:.0f} |",
          f"Total Peak Count: {total_peaks} |",
          f"Total Mem: {total_mb:.3f} MB")


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


def mzml_peak_count(mzml_file):
    """
    Return the total number of centroided peaks for all spectra in a mzML file
    """
    run = pymzml.run.Reader(mzml_file)
    total_peaks = 0
    for n, spec in enumerate(run):
        total_peaks += spectrum_peak_count(spec)
    return total_peaks


def mzml_peak_array_mb(mzml_file):
    """
    Return the size in MB all of the arrays of centroided peaks for all spectra in a mzML file
    """
    run = pymzml.run.Reader(mzml_file)
    total_mb = 0
    for n, spec in enumerate(run):
        total_mb += spectrum_peak_array_mb(spec)
    return total_mb


def create_spectrum_ml_df(spectrum):
    """
    Return a multilevel pandas data frame of centroided peaks for a spectrum

    First Column level: RT
    Second Column level: m/z, i
    Index: peak number in spectrum
    """
    rt = [spectrum.scan_time_in_minutes()]
    peaks = spectrum.peaks('centroided')
    columns = pd.MultiIndex.from_product([rt, ['m/z', 'i']], names=['RT', 'Peaks'])
    df = pd.DataFrame(peaks, columns=columns)
    return df


def create_mzml_ml_df(mzml_file):
    """
    Return a multilevel pandas data frame of all centroided peaks in an mzml file

    First Column level: RT
    Second Column level: m/z, i
    Index: peak number in spectrum
    """
    df = pd.DataFrame()
    run = pymzml.run.Reader(mzml_file)
    for n, spec in enumerate(run):
        spec_df = create_spectrum_ml_df(spec)
        df = pd.concat([spec_df, df], axis=1)
    return df


def create_spectrum_df(spectrum):
    """
    Return a pandas data frame of centroided peaks for a spectrum

    Columns: RT, m/z, i
    First Index Level: specID
    Second Index Level: peak number
    """
    mz_values = spectrum.mz.round(5)
    i_values = spectrum.i.round()
    rt = spectrum.scan_time_in_minutes()
    peak_count = spectrum_peak_count(spectrum)
    spec_id = [spectrum.ID]
    peak_list = list(range(peak_count))
    peak_index = pd.MultiIndex.from_product([spec_id, peak_list], names=['SpecID', 'Peak'])
    peaks = {'RT': rt,
             'mz': mz_values,
             'i': i_values}
    df = pd.DataFrame(peaks, index=peak_index)
    return df


def create_mzml_df(mzml_file):
    """
    Return a pandas data frame of all centroided peaks in an mzml file

    Columns: RT, m/z, i
    First Index Level: specID
    Second Index Level: peak number
    """
    df = pd.DataFrame()
    run = pymzml.run.Reader(mzml_file)
    for n, spec in enumerate(run):
        spec_df = create_spectrum_df(spec)
        df = pd.concat([df, spec_df])
    return df


def create_rt_index(mzml_file):
    """
    Return a pandas index of all rt / scan times in an mzml file
    """
    rt_list = []
    run = pymzml.run.Reader(mzml_file)

    # Build an index of RT values
    for n, spec in enumerate(run):
        rt = spec.scan_time_in_minutes()
        rt_list.append(rt)

    rt_index = pd.Index(rt_list, name='RT')
    return rt_index


def create_spectrum_flat_df(spectrum):
    """
    Return a flat pandas df of centroided peaks for a spectrum

    Columns: m/z
    Index: RT
    Values: i
    """
    mz_values = spectrum.mz.round(5)
    i_values = spectrum.i.round()
    rt = spectrum.scan_time_in_minutes()
    mz_columns = pd.Index(mz_values, name='m/z')
    rt_index = pd.Index([rt], name='RT')
    df = pd.DataFrame(index=rt_index, columns=mz_columns)
    df.loc[rt] = i_values
    return df


def create_mzml_flat_df(mzml_file):
    """
    Return a flat pandas data frame of all centroided peaks in an mzml file

    Columns: m/z
    Index: RT
    Values: i
    """
    df = pd.DataFrame()
    run = pymzml.run.Reader(mzml_file)
    for n, spec in enumerate(run):
        spec_df = create_spectrum_flat_df(spec)
        df = pd.concat([df, spec_df])
        # if n > 10:
        #     break
    return df


def save_df(df, filename):
    """
    Save a pandas data frame with pickle serialization and bzip2 compression
    """
    with bz2.open((filename+'.p.bz2'), "wb") as file:
        pickle.dump(df, file, pickle.HIGHEST_PROTOCOL)


def load_df(filename):
    """
    Load a pandas data frame previously saved with pickle serialization and bzip2 compression
    """
    with bz2.open(filename, "rb") as file:
        df = pickle.load(file)
    return df


def summarize_df(df):
    """
    Return a summary of rounded stats from a data frame

    """
    stats = df.describe().round()
    return stats


def create_spectrum_df_noise_removed(spectrum):
    """
    Return a pandas data frame of centroided peaks for a spectrum with noise removed

    Columns: RT, m/z, i
    First Index Level: specID
    Second Index Level: peak number
    """
    spectrum_nr = spectrum.remove_noise(mode='median', noise_level=None)
    mz_values = spectrum_nr.peaks('centroided')[:, 0].round(5)
    i_values = spectrum_nr.peaks('centroided')[:, 1].round()
    rt = spectrum_nr.scan_time_in_minutes()
    peak_count = spectrum_peak_count(spectrum_nr)
    spec_id = [spectrum_nr.ID]
    peak_list = list(range(peak_count))
    peak_index = pd.MultiIndex.from_product([spec_id, peak_list], names=['SpecID', 'Peak'])
    peaks = {'RT': rt,
             'mz': mz_values,
             'i': i_values}
    df = pd.DataFrame(peaks, index=peak_index)
    return df


def create_mzml_df_noise_removed(mzml_file):
    """
    Return a pandas data frame of all centroided peaks in an mzml file with noise removed

    Columns: RT, m/z, i
    First Index Level: specID
    Second Index Level: peak number
    """
    df = pd.DataFrame()
    run = pymzml.run.Reader(mzml_file)
    for n, spec in enumerate(run):
        spec_df = create_spectrum_df_noise_removed(spec)
        df = pd.concat([df, spec_df])
    return df


