import matplotlib.pyplot as plt
import csv
from configure import *

x = []
y = []

with open(sys.argv[1]) as csvfile:
     next(csvfile)
     plots = csv.reader(csvfile, delimiter=' ')
     for row in plots:
	 x.append(row[0])
	 y.append(int(row[1]))


#Chagne the line plot below to a scatter plot 

plt.scatter(x, y)
# Put the y-axis on a logarithmic scale 

plt.yscale('log')
#Strings
xlab = 'Time (us)'
ylab = 'Virtual Memory Address'
title = 'Trace'

# Add axis labels
plt.xlabel(xlab)
plt.ylabel(ylab)

#Add title
plt.title(title)

#show plot
plt.show()
