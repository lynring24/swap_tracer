import re
import time, calendar
from datetime import datetime



MICROSEC_PATTERN = "(\d+:\d{2}:\d{2}\.\d{6}) (.+)"

def is_valid_ms(line):
    matched= re.compile(MICROSEC_PATTERN).search(line)
    return matched
