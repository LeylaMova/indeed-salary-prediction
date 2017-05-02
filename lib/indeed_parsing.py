import pandas as pd
import requests
from bs4 import BeautifulSoup





url = "http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l={}&start={}"

def extract_posts(max_results_per_city, cities=[]):
    """
       Extract the city, state, company, salary, summary and title from posts on indeed and return in a DataFrame. max_results_per_city is accepts integer and cities accepts a list of cities.
    
    """
    
    max_results_per_city = max_results_per_city  

    posts = []
    for city in cities:
        for start in range(0, max_results_per_city, 10):
            response = requests.get(url.format(city, start))
            soup = BeautifulSoup(response.content, "lxml")
            results = soup.findAll('div', { "class" : "result" })
            
            for div in results:
                if div:
                    try:
                        post = {}
                        post['city'] = div.find('span', {'class' : 'location'}).text.split(',')[0]
                        post['state'] = div.find('span', {'class' : 'location'}).text.split(',')[1].split()[0]
                        post['company'] = div.find('span', {'class' : 'company'}).text.strip()
                        post['salary'] = div.find_all('nobr')[0].text
                        post['summary'] = div.find('span', {'class' : 'summary'}).text.strip()
                        post['title'] = div.find('a', {'data-tn-element' : 'jobTitle'}).text.strip()
                        posts.append(post)
        
                    except:
                        pass
            
    return pd.DataFrame.from_records(posts)


def extract_posts_wo_salary(max_results_per_city, cities=[]):
    """
       Extract the city, state, company, summary and title from posts on indeed and return in a DataFrame. max_results_per_city is accepts integer and cities accepts a list of cities.
    
    """
    
    max_results_per_city = max_results_per_city  

    posts = []
    for city in cities:
        for start in range(0, max_results_per_city, 10):
            response = requests.get(url.format(city, start))
            soup = BeautifulSoup(response.content, "lxml")
            results = soup.findAll('div', { "class" : "result" })
            
            for div in results:
                if div:
                    try:
                        post = {}
                        post['city'] = div.find('span', {'class' : 'location'}).text.split(',')[0]
                        post['state'] = div.find('span', {'class' : 'location'}).text.split(',')[1].split()[0]
                        post['company'] = div.find('span', {'class' : 'company'}).text.strip()
                        post['summary'] = div.find('span', {'class' : 'summary'}).text.strip()
                        post['title'] = div.find('a', {'data-tn-element' : 'jobTitle'}).text.strip()
                        posts.append(post)
        
                    except:
                        pass
            
    return pd.DataFrame.from_records(posts)



    
    
    
    
    
    
    
    














    
    