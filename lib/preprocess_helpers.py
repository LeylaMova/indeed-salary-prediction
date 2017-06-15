import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction import stop_words


def clean_salary(row):
    """
       Converts string salary or salary range to average salary in integer.
       
       Arguments:
       
           row: pandas apply method       
       
       Returns converted row
    
    """
    
    row = row.replace(',','')
    if 'year' in row:
        row = re.findall(r'\d+', row)
        row = round(np.mean([int(num) for num in row]))
    else:
        row = np.nan
    
    return row


def clean_text(row):
    """
       Converts text to raw text with no punctuations or numbers.
       
       Arguments:
       
           row: pandas apply method       
       
       Returns converted row
    
    """
    
    regex = re.compile("[^a-zA-Z0-9']")
    row = row.lower()
    row = regex.sub(' ', row)
    row = ' '.join(row.split())
    regex = re.compile("\'")
    row = regex.sub('', row)

    return row


def standardize(row):
    """
       Standardize text variations: 'post doc'|'postdoctoral'|'post doctoral' -> 'phd',
                                    'sr' -> 'senior', 'jr' -> 'junior', 'svp' -> 'senior vp',
                                    'ai' -> 'artificial intelligence', 'ml' -> 'machine learning',
                                    'vice president' -> 'vp'
       
       Arguments:
       
           row: pandas apply method       
       
       Returns converted row
    
    """
    
    row = row.replace(r'post doc', 'phd').replace(r'postdoctoral', 'phd').replace(r'post doctoral', 'phd')
    row = row.replace(r'sr','senior').replace(r'jr','junior').replace(r'ai','artificial intelligence')
    row = row.replace(r'ml','machine learning').replace(r'scientists','scientist')
    row = row.replace(r'svp','senior vp').replace(r'analytics','analytic')
    row = row.replace(r'vice president','vp').replace(r'analysts','analyst')

    return row


def combine_text(row):
    
    city = row['city']
    summary = row['summary']
    title = row['title']
    text = city + ' ' + summary + ' ' + title
    
    return text


def remove_stop_words(row):

    words = row.split()
    clean = []
    for word in words:
        if word not in stop_words:
            clean.append(word)
            
    return ' '.join(clean)










