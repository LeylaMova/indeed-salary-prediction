import pandas as pd
from lib.preprocess_helpers import clean_salary, clean_text, standardize, combine_text, remove_stop_words


def preprocess_w_salary(df):
    
    df['salary'] = df['salary'].apply(clean_salary)
    df.dropna(inplace=True)
    df['company'] = df['company'].apply(clean_text)
    df['summary'] = df['summary'].apply(clean_text)
    df['title'] = df['title'].apply(clean_text)
    df['title'] = df['title'].apply(standardize)
    df['summary'] = df['summary'].apply(standardize)
    df['text'] = df.apply(combine_text, axis=1)
    
    return df


def preprocess_wo_salary(df):
    
    df['company'] = df['company'].apply(clean_text)
    df['summary'] = df['summary'].apply(clean_text)
    df['title'] = df['title'].apply(clean_text)
    df['title'] = df['title'].apply(standardize)
    df['summary'] = df['summary'].apply(standardize)
    df['text'] = df.apply(combine_text, axis=1)
    
    return df