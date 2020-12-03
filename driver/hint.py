import pandas as pd

def hint():
    objects = pd.read_csv('./su3imp.out', header=None)
    objects.columns = ['fname', 'function', 'varname', 'address', 'size']
    objects = objects.drop_duplicates(keep='first').sort_values('size', ascending = 0 )
    #objects['count'] = objects.groupby('varname').transform('count')

    print objects
    objects.to_csv('./info.csv')



if __name__ == "__main__":
    hint()
