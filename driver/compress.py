import os
import sys
import pandas as pd


with open('./rsyslog.dat', 'r') as rsyslogs:
    DUMP = []
    for rsyslog in rsyslogs:
        df = pd.read_csv(rsyslog[:-1])
        df = df[df['mode'] == 'map']
        df = df.drop('mode', axis=1)


            
