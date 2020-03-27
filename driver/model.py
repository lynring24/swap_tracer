import numpy as np
import pandas as pd 
from pandas import DataFrame
from sklearn.cluster import KMeans
import csv 
from utility import *

<<<<<<< HEAD
=======
def build(n_clusters, df):
    kmeans = KMeans(n_clusters=n_clusters, max_iter=100, n_init=10, random_state=0)
    Z = kmeans.fit_predict(df)
    return kmeans, Z 

>>>>>>> 026724062b5c2746723de2fd013f16cde949a1a3

def cluster():
    with open(get_path('total'), 'r+') as file:
        reader = csv.reader(file, delimiter=',')
        data = dict()
        lines = []
        for line in reader:
            data.setdefault('time', []).append(line[0])
            data.setdefault('vas', []).append(line[1])
            lines.append(line)
        df = DataFrame(data, columns=['time', 'vas'])
<<<<<<< HEAD

        kmeans = KMeans(n_clusters=get_class(),  max_iter=100, n_init=10, random_state=0)
        label = kmeans.fit_predict(df)
        
=======
        
        inertias= []
        diff = pow(2,30) 
        threshold = pow(2,10)

        for num in xrange(1, 5):
            kmeans, label = build(num, df)
            inertias.append(kmeans.inertia_)             
            if num != 1 and  inertias[num-1] - inertias[num-2] < threshold:
               break;

        opt = inertias.index(min(inertias))+1 
        set_class(opt)
>>>>>>> 026724062b5c2746723de2fd013f16cde949a1a3
        with open(get_path('labeled'), 'w') as labeled:
             writer = csv.writer(labeled, delimiter=',')
	     for idx in range (0, len(lines)): 
                 lines[idx].insert(0, label[idx])
                 writer.writerow(lines[idx])
<<<<<<< HEAD
       
       
=======
>>>>>>> 026724062b5c2746723de2fd013f16cde949a1a3
