import pandas as pd
import numpy as np
import re


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
        row = np.mean([int(num) for num in row])
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
    
    regex = re.compile("[^a-zA-Z.']")
    row = row.encode("utf8").lower()
    row = regex.sub(' ', row)
    row = ' '.join(row.split())
    regex = re.compile("\.|\'")
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


correct_city = {"Dania Beach": "Miami Suburb", "Silver Spring": "Washington Suburb", "Arlington": "Washington Suburb", "Pasadena": "Los Angeles Suburb", "Gilbert": "Phoenix Suburb", "Boulder": "Denver Suburb", "Reston": "Washington Suburb", "Redmond": "Seattle Suburb", "Scottsdale": "Phoenix Suburb", "Bellevue": "Seattle Suburb", "Berkeley": "San Francisco Suburb", "League City": "Houston Suburb", "Ambler": "Philadelphia Suburb", "Hidden Hills": "Los Angeles Suburb", "Rosemont": "Chicago Suburb", "Norcross": "Atlanta Suburb", "Calabasas": "Los Angeles Suburb", "Richardson": "Dallas Suburb", "Valley Stream": "New York Suburb", "Fairfax": "Washington Suburb", "Fort Meade": "Washington Suburb", "Alexandria": "Washington Suburb", "Gaithersburg": "Washington Suburb", "Northbrook": "Chicago Suburb", "Wayne": "Philadelphia Suburb", "Laurel": "Washington Suburb", "Santa Monica": "Los Angeles Suburb", "Evanston": "Chicago Suburb", "Plantation": "Miami Suburb", "Downers Grove": "Chicago Suburb", "Manhattan": "New York Suburb", "Springfield": "Washington Suburb", "College Park": "Washington Suburb", "Northridge": "Los Angeles Suburb", "Jersey City": "New York Suburb", "Tempe": "Phoenix Suburb", "Cherry Hill": "Philadelphia Suburb", "Aurora": "Denver Suburb", "Irving": "Dallas Suburb", "San Mateo": "San Francisco Suburb", "El Segundo": "Los Angeles Suburb", "Torrance": "Los Angeles Suburb", "Malvern": "Philadelphia Suburb", "Beaverton": "Portland Suburb", "Emeryville": "San Francisco Suburb", "Paramus": "New York Suburb", "Wilmington": "Philadelphia Suburb", "Horsham": "Philadelphia Suburb", "Columbia": "Washington Suburb", "Redwood City": "San Francisco Suburb", "San Francisco Bay Area": "San Francisco Suburb", "Roswell": "Atlanta Suburb", "Beverly Hills": "Los Angeles Suburb", "Coral Gables": "Miami Suburb", "Oakland": "San Francisco Suburb", "Kenilworth": "New York Suburb"}


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


def extract_keywords_into_dummies(df, col, *words):
    """
       Extracts words from text and converts into binary.
       
       Arguments:
       
           df: pandas DataFrame
           col: specific column
           words: string of words
       
       Returns DataFrame with all carigorical dummies
    
    """   
    col = df[col]
    for word in words:
        df[word] = pd.get_dummies(col.str.extract('({})'.format(word), expand=False))
    
    return df
    

def is_keyword_in_title_or_summary(row, words=[]):
    """
       Extracts words from summary and title column and converts into binary.
       
       Arguments:
       
           row: pandas apply method
           words: string of words
       
       Returns binary
    
    """   
    summary = row['summary']
    title = row['title']

    if any(elm in summary or elm in title for elm in words):        
        return 1

    else:
        return 0
















