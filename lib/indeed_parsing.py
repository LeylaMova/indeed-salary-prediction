import pandas as pd
import requests
import time
from collections import defaultdict
from bs4 import BeautifulSoup
from lib.parsing_helpers import keyword_query, get_title_from_result, get_company_from_result, get_location_from_result, get_summary_from_result, get_salary_from_result


def extract_posts_w_salary_to_df(keyword=[], city_set=[], max_results_per_city=int):
    """
       Extracts city, state, company, salary, summary and title from posts on indeed.
       
       Arguments:
       
           max_results_per_city:  integer 
           cities: list of strings
             
       Returns a Pandas DataFrame 
    
    """
    url = keyword_query(keyword)  
    
    job_post = defaultdict(list)
    for city in city_set:
        
        for start in range(0, max_results_per_city, 10):
            page = requests.get(url.format(city, start))
            time.sleep(1)  #ensuring at least 1 second between page grabs
            soup = BeautifulSoup(page.text, 'html.parser')
                       
            for div in soup.find_all(name='div', attrs={'class':'row'}):
                try:
                    if get_salary_from_result(div):
                        job_post['city'].append(city)
                        job_post['title'].append(get_title_from_result(div))
                        job_post['company'].append(get_company_from_result(div))
                        job_post['location'].append(get_location_from_result(div))
                        job_post['summary'].append(get_summary_from_result(div))
                        job_post['salary'].append(get_salary_from_result(div))
                except:
                    pass
    
    df = pd.DataFrame.from_records(job_post)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df


def extract_posts_to_df(keyword=[], city_set=[], max_results_per_city=int):
    """
       Extracts city, state, company, summary and title from posts on indeed.
       
       Arguments:
       
           max_results_per_city:  integer 
           cities: list of strings
       
       
       Returns a Pandas DataFrame 
    
    """
    
    url = keyword_query(keyword)  
    
    job_post = defaultdict(list)
    for city in city_set:
        
        for start in range(0, max_results_per_city, 10):
            page = requests.get(url.format(city, start))
            time.sleep(1)  #ensuring at least 1 second between page grabs
            soup = BeautifulSoup(page.text, 'html.parser')
                       
            for div in soup.find_all(name='div', attrs={'class':'row'}):
                job_post['city'].append(city)
                job_post['title'].append(get_title_from_result(div))
                job_post['company'].append(get_company_from_result(div))
                job_post['location'].append(get_location_from_result(div))
                job_post['summary'].append(get_summary_from_result(div))
    
    df = pd.DataFrame.from_records(job_post)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df

    
    
    
    
    
    
    
    














    
    