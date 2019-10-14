
""""
key

* Define location of example data and expected values for unit tests

"""


from tests.config import MSfileKey, TestMSspectrum, TestMSpeak


# Location of example MS data saved as mzML files
mzml_files_list = ["data/mzML/EP0482.mzML",
                   "data/mzML/EP2421.mzML",
                   "data/mzML/EP2536.mzML"]


# Provide correct values for the example MS data
# Ensure to name the key '<run_id>_key' in the module namespace
#   for key to be assigned during test fixture creation

EP0482_key = MSfileKey(
    run_id='EP0482',
    run_date='2017-06-12T17:36:24Z',
    ms_file_version='1.1.0',
    spectrum_count=621,
    peak_count=1166167,
    tic_sum=65811135712.0)


EP2421_key = MSfileKey(
    run_id='EP2421',
    run_date='2017-06-28T04:10:21Z',
    ms_file_version='1.1.0',
    spectrum_count=651,
    peak_count=1430013,
    tic_sum=103151911964.0)


EP2536_key = MSfileKey(
    run_id='EP2536',
    run_date='2017-06-10T12:52:27Z',
    ms_file_version='1.1.0',
    spectrum_count=618,
    peak_count=1156165,
    tic_sum=80343932406.0)


# Provide correct spectrum values for MS files listed above
spectrum_list = [
    TestMSspectrum(run_id='EP0482',
                   spec_id=289,
                   rt=3.0089726,
                   peak_count=1486,
                   tic=32847246.0,
                   ms_lvl=1,
                   filters='FTMS + p ESI Full ms [115.0000-1000.0000]'),
    TestMSspectrum(run_id='EP0482',
                   spec_id=1529,
                   rt=15.982354,
                   peak_count=2826,
                   tic=73259136.0,
                   ms_lvl=1,
                   filters='FTMS + p ESI Full ms [115.0000-1000.0000]'),
    TestMSspectrum(run_id='EP2421',
                   spec_id=299,
                   rt=3.0188414,
                   peak_count=1745,
                   tic=46977344.0,
                   ms_lvl=1,
                   filters='FTMS + p ESI Full ms [115.0000-1000.0000]'),
    TestMSspectrum(run_id='EP2421',
                   spec_id=1599,
                   rt=15.998312,
                   peak_count=3285,
                   tic=174533700.0,
                   ms_lvl=1,
                   filters='FTMS + p ESI Full ms [115.0000-1000.0000]'),
    TestMSspectrum(run_id='EP2536',
                   spec_id=291,
                   rt=3.0137982,
                   peak_count=1642,
                   tic=26710684.0,
                   ms_lvl=1,
                   filters='FTMS + p ESI Full ms [115.0000-1000.0000]'),
    TestMSspectrum(run_id='EP2536',
                   spec_id=1525,
                   rt=15.992136,
                   peak_count=2764,
                   tic=81435368.0,
                   ms_lvl=1,
                   filters='FTMS + p ESI Full ms [115.0000-1000.0000]')]


# Provide correct peak values for MS files listed above
peak_list = [
    TestMSpeak(run_id='EP0482',
               spec_id=289,
               peak_number=309,
               rt=3.0089726,
               mz=156.96542,
               i=24634.966796875),
    TestMSpeak(run_id='EP0482',
               spec_id=1529,
               peak_number=2345,
               rt=15.982354,
               mz=497.39899,
               i=21550.2109375),
    TestMSpeak(run_id='EP2421',
               spec_id=299,
               peak_number=309,
               rt=3.0188414,
               mz=141.94194,
               i=29752.486328125),
    TestMSpeak(run_id='EP2421',
               spec_id=1599,
               peak_number=349,
               rt=15.998312,
               mz=153.11383,
               i=102251.484375),
    TestMSpeak(run_id='EP2536',
               spec_id=291,
               peak_number=309,
               rt=3.0137982,
               mz=149.95224,
               i=5651.51513671875),
    TestMSpeak(run_id='EP2536',
               spec_id=1525,
               peak_number=1255,
               rt=15.992136,
               mz=280.22473,
               i=20079.5625)]

