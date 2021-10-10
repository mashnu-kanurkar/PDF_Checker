import datetime
from inspect import currentframe, getframeinfo
from datetime import date

def log(level, log_msg):
    today = date.today()
    log_file = '.\\App_config\\log\\log_{}.txt'.format(today)
    try:
        log_file = open(log_file, 'a')
        now = datetime.datetime.now()
        log_file.write('{}-     {}-     log_msg: {}\n'.format(level, now.strftime("%Y-%m-%d %H:%M:%S"), log_msg))
        log_file.close()

    except FileNotFoundError:
        with open(log_file, 'w') as log_file:
            now = datetime.datetime.now()
            log_file.write('{}-     {}-     log_msg: {}\n'.format(level, now.strftime("%Y-%m-%d %H:%M:%S"), log_msg))
    except Exception as e:
        raise e
DEBUG = 'DEBUG'
INFO = 'INFO'
INFO_ERROR = 'INFO_E'
SPEC_ERROR = 'SPEC_E'
EXCEPTION = 'EXCE'

def get_filename_and_line():
    frameinfo = getframeinfo(currentframe())
    return frameinfo.filename, frameinfo.lineno


