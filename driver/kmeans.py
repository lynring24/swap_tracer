import numpy as np
import pandas as pd 
from pandas import DataFrame
from sklearn.cluster import KMeans
import sys
import csv 

def build(n_clusters, df):
    kmeans = KMeans(n_clusters=n_clusters, max_iter=100, n_init=10, random_state=0)
    Z = kmeans.fit_predict(df)
    return kmeans, Z 



def cluster():
    
    rsyslog = pd.read_csv("./rsyslog.csv", usecols=['timestamp', 'address'])
    print(rsyslog.head(5))
        
    inertias= []
    threshold = pow(2, 5)

    for num in xrange(1, 5):
        kmeans, label = build(num, rsyslog)
        inertias.append(kmeans.inertia_)             
        #if num != 1 and  inertias[num-1] - inertias[num-2] < threshold:
        #   break;

    opt = inertias.index(min(inertias))+1 
    print(inertias)
    print(opt)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        cluster()
    else:
        print("Usage : python kmeans.py")

    print("\n[Finish]")
