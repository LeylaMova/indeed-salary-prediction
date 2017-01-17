"""
indeed_parsing.py
Creator: Arun Ahuja

This was the script used to generate the sample file

"""


from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd


url = "http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"


def extract_text(el):
    if el:
        return el.text.strip()
    else:
        return ''      

def get_company_from_result(result):
    return extract_text(result.find('span', {'class' : 'company'}))

def get_location_from_result(result):
    return extract_text(result.find('span', {'class' : 'location'}))

def get_summary_from_result(result):
    return extract_text(result.find('span', {'class' : 'summary'}))

def get_title_from_result(result):
    return result.find('a', {'data-tn-element' : 'jobTitle'}).text.strip()

def get_salary_from_result(result):
    salary_table = result.find('td', {'class' : 'snip'})
    if salary_table:
        snip = salary_table.find('nobr')
        if snip:
            return snip.text.strip()

    return None


def extract_salary_average(salary_string):
    regex = r'\$([0-9]+,[0-9]+)'
    matches = re.findall(regex, salary_string)
    return np.mean([float(salary.replace(',', '')) for salary in matches ])


url = "http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l={}&start={}"
rows = []

for city in set(['Palo+Alto', 'San+Diego', 'Indianapolis', 
    'New+York', 'Chicago', 'San+Francisco', 'Austin', 'Seattle', 
    'Los+Angeles', 'Philadelphia', 'Atlanta', 'Dallas', 'Pittsburgh', 
    'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 
    'Charleston', 'Boston', 'Cleveland']):
    for start in range(10, 15000, 10):
        r = requests.get(url.format(city, start))
        soup = BeautifulSoup(r.content)
        results = soup.findAll('div', { "class" : "result" })
        for result in results:
            if result:
                row = {}
                row['title'] = get_title_from_result(result)
                row['company'] = get_company_from_result(result)
                row['summary'] = get_summary_from_result(result)
                row['salary'] = get_salary_from_result(result)
                row['city'] = city
                rows.append(row)

data = pd.DataFrame.from_records(rows)


# Drop duplicates and clean up non-annual salaries
data = data.drop_duplicates()
salary_data = data[data.salary.notnull()]
salary_data = salary_data[~(salary_data.salary.astype('str').str.contains('hr'))]
salary_data = salary_data[~(salary_data.salary.astype('str').str.contains('hour'))]
salary_data = salary_data[~(salary_data.salary.astype('str').str.contains('week'))]
salary_data = salary_data[~(salary_data.salary.astype('str').str.contains('wk'))]
salary_data = salary_data[~(salary_data.salary.astype('str').str.contains('month'))]


salary_data.to_csv('indeed-scraped-job-postings.csv', index=False)
