#!/Users/Leyla/anaconda/bin/python
import pandas as pd
from lib.preprocessing import clean_salary, clean_text, standardize, extract_keywords_into_dummies, is_keyword_in_title_or_summary, map_city, suburban_vs_city
from sklearn.externals import joblib


def predict_salary(df):
    dummy_to_range = {'0':'$24000 to $69673', '1':'$70000 to $160000', '2':'$162500 to $300000'}
    model = joblib.load('data/model.pkl')
    
    df['summary'] = df['summary'].apply(clean_text)
    df['title'] = df['title'].apply(clean_text)
    df['city'] = df['city'].astype(str)
    df['title'] = df['title'].apply(standardize)
    df['summary'] = df['summary'].apply(standardize)
    df['city'] = df.apply(map_city, axis=1)
    
    df['city_suburb'] = df['city'].apply(lambda x: 1 if 'Suburb' in x else 0)
    df = df.join(pd.get_dummies(df['city'].apply(suburban_vs_city)))
    df = extract_keywords_into_dummies(df, 'title','research','analyst','research analyst',
                                   'scientist','associate','specialist','phd',
                                   'technician','fellow','senior','senior research',
                                   'laboratory','analyst research','research associate',
                                   'data scientist','engineer','machine learning',
                                   'senior data','software','lead','data engineer',
                                   'data science','quantitative','science','director',
                                   'director data','data science')
    df = extract_keywords_into_dummies(df, 'summary','analysis','quality','interpret',
                                   'analyze','collection','management','data collection',
                                   'environmental','assist','entry','statistical',
                                   'data analysis','python','analytic','modeling','big',
                                   'mining','big data')
    
    X = df.drop(['city','company','summary','title'], axis=1)
    df['percentile_class'] = model.predict(X)
    df['salary_range'] = df['percentile_class'].apply(lambda x: dummy_to_range[str(x)] if str(x) in dummy_to_range.keys() else np.nan)
    
    
    return df[['city','company','summary','title','salary_range','percentile_class']]
    
    
    
    
    

    