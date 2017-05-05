import pandas as pd
import json


with open('data/correct_city.json', 'r') as fp:
    correct_city = json.load(fp)
    

def map_city(row):
    """
       Maps suburban cities to city.
       
       Arguments:
       
           row: pandas apply method       
       
       Returns converted row
    
    """
    city = row['city']

    if city in correct_city.keys():
        return correct_city[city]
        
    else:
        return city
    
    
def suburban_vs_city(row):
    """
       Convert suburban vs city into binary.
       
       Arguments:
       
           row: pandas apply method       
       
       Returns converted row
    
    """
    if 'Suburb' in row:
        if len(row.split()) > 2:
            row = row.split()[0] + ' ' + row.split()[1]
        else:
            row = row.split()[0]
    else:
        row
    return row




























