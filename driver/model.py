import numpy as np
import pandas as pd 
from pandas import DataFrame
from sklearn.cluster import KMeans
import csv 
from utility import *


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

        kmeans = KMeans(n_clusters=get_class(),  max_iter=100, n_init=10, random_state=0)
        label = kmeans.fit_predict(df)
        
        with open(get_path('labeled'), 'w') as labeled:
             writer = csv.writer(labeled, delimiter=',')
	     for idx in range (0, len(lines)): 
                 lines[idx].insert(0, label[idx])
                 writer.writerow(lines[idx])
       
       
