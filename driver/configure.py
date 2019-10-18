import os, sys, platform
import re, traceback
import time, calendar
from datetime import datetime, timedelta


CSV_PATTERN='%b%d%H%M%S'
DATE_PATTERN="%Y-%m-%dT%H:%M:%S.%f"
MICROSEC_PATTERN = "(\d+:\d{2}:\d{2}\.\d{6}) (.+)"
BLOCK_PATTERN = "(\d+.\d{6}) (.+)"

BLOCK=1024
PAGE_SIZE=4096
DIGIT_THRESHOLD = 14


def is_valid_ms(line):
    matched= re.compile(BLOCK_PATTERN).search(line)
    return matched

def get_current_log_path():
    LOG_DIR_PATH = None
    try :
         print "hellpo"
         LOG_DIR_PATH=os.environ.get('CURRENT_LOG')
    except KeyError:
         print "environment setting failure"
	 sys.exit(1)
    return LOG_DIR_PATH
