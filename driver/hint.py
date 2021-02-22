import pandas as pd
import sys

def hint():
    objects = pd.read_csv(sys.argv[1], header=None)
    objects.columns = ['fname', 'function', 'varname', 'address', 'size']
    objects = objects.drop_duplicates(keep='first').sort_values('address', ascending = 0)

    print( objects.head(5))
    objects.to_csv('./info.csv')



if __name__ == "__main__":
    hint()
