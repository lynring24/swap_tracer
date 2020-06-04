import os
import pandas as pd
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt

# timestamp, moode, vma 
logfile = "/home/hrchung/benchmarks/linear/2020-06-04T01:22:03.960323/merge.csv"

csvfile = pd.read_csv(logfile)

labels = csvfile['mode'].unique() 
color = {'out':'blue', 'in': 'orange', 'map':'green', 'writepage':'brown'}

fig, ax = plt.subplots()

for label in labels:
    data = csvfile[csvfile['mode']==label]
    print data.shape
    ax.plot(data['timestamp'].to_numpy(), data['address'].to_numpy(), label=label, color=color.get('label'))
ax.legend(loc='best')

plt.xlabel('timestamp (usec)')
plt.ylabel('virtual page number')
plt.savefig(logfile[:-9]+'scatter.pdf',format='pdf', dpi=150)
# plt.show()
