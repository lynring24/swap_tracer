import matplotlib.pyplot as plt
import csv
import glob 
from configure import *


def to_pdf():
    global logs
    logs = glob.glob(get_path('head')+'/*.log')

    fig = plt.figure()
    plt.rcParams['figure.figsize'] = [10,10]
    plt.rcParams["font.weight"] = "bold"
    plt.subplots_adjust (hspace=0.5)

    fontdicty={'fontsize': 20,
          'weight' : 'bold',
          'verticalalignment': 'baseline',
          'horizontalalignment': 'center'}

    fontdictx={'fontsize': 20,
          'weight' : 'bold',
          'horizontalalignment': 'center'}




    fig.suptitle('swap timestamps of $ %s %s'%(str(get_mem_limit()),  get_command()), fontsize=25,fontweight="bold", color="black",  position=(0.5,1.0))

    grids=[]
    grid_idx = 0
    for side in reversed(area):
        if side != 'total' and get_path( side ) in logs:
           with open (get_path(side)) as csvfile:
		x = []
		y = []
                plots = csv.reader(csvfile, delimiter=',')
                for row in plots:
	           x.append(row[0])
	           y.append(int(row[1]))
 
                grids.append(fig.add_subplot(412, sharex=grids[0]))
                grids[grid_idx].scatter(x, y, c='orange')
                grid_idx+=1
               
           grids[0].set_ylabel('VPN (Virtual Page Number)', fontdict=fontdicty, position=(-0.3, -0.2))
           grids[-1].set_xlabel('Duration (sec)', fontdict=fontdictx)
    plt.show()
    f.savefig(get_path('pdf'),bbox_inches='tight')         



