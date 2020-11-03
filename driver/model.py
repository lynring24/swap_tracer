import numpy as np
import pandas as pd 
from pandas import DataFrame
from sklearn.cluster import KMeans
import csv 
from utility import *

def build(n_clusters, df):
    kmeans = KMeans(n_clusters=n_clusters, max_iter=100, n_init=10, random_state=0)
    Z = kmeans.fit_predict(df)
    return kmeans, Z 



def cluster(dir_path):
    
    rsyslog.pd.read_csv(dir_path+"/rsyslog.csv")
        
    inertias= []
    threshold = pow(2,10)

    for num in xrange(1, 5):
        kmeans, label = build(num, rsyslog)
        inertias.append(kmeans.inertia_)             
        if num != 1 and  inertias[num-1] - inertias[num-2] < threshold:
           break;

    opt = inertias.index(min(inertias))+1 

