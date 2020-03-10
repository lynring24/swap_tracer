import numpy as np
import pandas as pd 
from pandas import DataFrame
from sklearn.cluster import KMeans
import csv 
from utility import *

def build():
    with open(get_path('total')) as file:
        reader = csv.reader(file, delimiter=',')
        data = dict()
        for line in reader:
            data.setdefault('time', []).append(line[0])
            data.setdefault('vas', []).append(line[1])
        
        df = DataFrame(data, columns=['time', 'vas'])

        wcss = [] 
        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
            kmeans.fit(df)
            wcss.append(kmeans.inertia_)
        print wcss
        index_min = min(xrange(len(wcss)), key=wcss.__getitem__)
        print wcss[index_min]

        kmeans = KMeans(n_clusters=index_min, init='k-means++', max_iter=300, n_init=10, random_state=0)
        
