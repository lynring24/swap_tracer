import re, sys
import time 

def convert2time(timeline):
    return time.strptime (timeline, '%H:%M:%S')

if __name__ == "__main__":
    row_num = 0
    cmptime = convert2time(sys.argv[2])
    output = open(sys.argv[1]+'.csv', "w")
    with open(sys.argv[1], "r") as file:
        for line in file:
            matched = re.compile('(.*:.*:\d{2}) .*').search(line)
            if matched is None:
                continue

            comperand = convert2time(matched.group(1))
            if comperand < cmptime :
                output.write(line)

                row_num+=1


