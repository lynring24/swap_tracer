
import sys

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
	formatStr = "{0:." + str(decimals) + "f}"
	percent = formatStr.format(100 * (iteration / float(total)))
        filledLength = int(round(barLength * iteration / float(total)))
	bar = '#' * filledLength + '-' * (barLength - filledLength)
	sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
	if iteration == total:
	    sys.stdout.write('\n')
        sys.stdout.flush()



UNIT=1000
total=0
for i in range(0, 10*UNIT*UNIT):
      printProgress(i, 10*UNIT*UNIT, 'Progress:', 'Complete', 1, 50)
print "\n[End]"
