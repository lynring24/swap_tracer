import pandas as pd
import sys
import numpy as np 
import matplotlib.pyplot as plt
#import matplotlib
#matplotlib.use('Agg')

df = pd.read_csv(sys.argv[1], names=['time', 'address'])

def scatterplot(df, x_dim, y_dim):
    x = df[x_dim]
    y = df[y_dim]
   
#    plt.plot( x, y )
    plt.savefig('../graph/'+sys.argv[1]+'.png')
    

scatterplot(df, 'time', 'address')
 
