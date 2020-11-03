import os
import pandas as pd
import matplotlib as mpl
import numpy 
from multiprocess import Pool, cpu_count

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


labels={'in':'swap-in','map':'memory map', 'fault':'page fault','out':'swap-out', 'writepage':'file I/O', 'handle_mm':'total page fault', 'allocation':'allocation'}
colors={'in':'red', 'out':'blue', 'map':'green', 'fault':'purple', 'allocation':'brown', 'handle_mm':'magenta' }
zorders={'fault':5, 'map':10, 'out':0, 'handle_mm':3}


def plot_out(dir_path, mean_time):

    #maps = pd.read_csv(dir_path+"/maps.csv", sep='\s+', header=None) 
    maps = pd.read_csv(dir_path+"/maps.csv") 
    #maps.columns = ['layout', 'perm' , 'offset', 'duration', 'inode', 'pathname']
    #maps = maps.join(maps['layout'].str.split('-', expand=True).add_prefix('layout'))
    #maps = maps.drop('layout', 1)

    maps['pathname'] = maps['pathname'].fillna('anon')
    #pname=['array[0]','array[100000]','array[1048575]','loop','idx','heap[0]','heap[100000]','heap[1048575]']
    pname=['a[0]','a[100000]','a[1048575]','loop','idx','h[0]','h[100000]','h[1048575]']
    maps['layout0'] = maps.apply(lambda row : int(row['layout0'], 16) if row['pathname'] in pname else int(row['layout0']), axis=1)
    #maps['layout1'] = maps['layout1'].fillna('0')
    maps['layout1'] = maps.apply(lambda row : int(row['layout1'], 16) if row['pathname'] in pname else int(row['layout1']), axis=1)
    maps['yaxis'] = maps['layout0'].apply(lambda x:format(x, '#04x'))
    maps[['pathname','layout0','layout1']].to_csv('./report.csv')

    fig = plt.figure()
    axes= plt.subplot(111)
    
    axes.set_yticks(maps.layout0)
    axes.set_yticklabels(maps.yaxis)
    
    xarea =0
    fix = ['[stack]', '[heap]', 'anon']
    for index, row in maps.iterrows():
        if row['pathname'] == '[vsyscall]':
            continue    

        #if row['layout0'] <= int('94898210406400'):
        #if 139785345720320<=row['layout0'] and row['layout0'] <= int('139785356320768'):
        if 140735677308928 <=row['layout0'] and row['layout0'] <= int('140735678197760'):
            if row['pathname'] in fix:
                axes.add_patch(mpl.patches.Rectangle((0, row['layout0']),1, row['layout1']-row['layout0'],color=numpy.random.rand(3,),zorder=0))
            else:
                axes.hlines(row['layout0'], label=row['pathname'], xmin=0, xmax=1, colors=numpy.random.rand(3,))
            xarea = numpy.random.rand()%4
            axes.text(xarea,row['layout0'],row['pathname'], va='center')


    #chartBox = axes.get_position()
    #axes.set_position([chartBox.x0*1.5, chartBox.y0, chartBox.width*0.6, chartBox.height])

    plt.legend(title='pathname', bbox_to_anchor=(1.05, 1), loc='upper center', fontsize='xx-small') 

    #plt.suptitle('start of memory layout (7f224fe06000 ~ 7f2250822000 ) ')
    plt.suptitle('start of memory layout ( 7fff940da000 ~ 7fff941b3000 ) ')
    #plt.suptitle('start of memory layout ( ~ 564f361f0000 ) ')
    #plt.suptitle('start of memory layout')
    plt.xlabel('timestamp')
    plt.ylabel('Virtual Address')

    plt.savefig('./heap.png', format='png')


    
plot_out('.', 0)
