from bs4 import BeautifulSoup


def keyword_query(keyword):
    """
    
    Takes Indeed parameters, converts, and returns it into appropriate query format. 
    
    """
    url = "http://www.indeed.com/jobs?q="
    for words in keyword:
        for word in words.split():
            url += word + '+'
    
    url = url + '&l={}&start={}'
    
    return url


def extract_text(query):
    if query:
        return query.text.strip()
    else:
        return None      

    
def get_title_from_result(div):
    return extract_text(div.find(name='a', attrs={'data-tn-element':'jobTitle'}))


def get_company_from_result(div):
    return extract_text(div.find('span', {'class' : 'company'}))


def get_location_from_result(div):
    return extract_text(div.find('span', {'class' : 'location'}))


def get_summary_from_result(div):
    return extract_text(div.find('span', {'class' : 'summary'}))


def get_salary_from_result(div):
    
    if div.find('nobr'):        
        return div.find('nobr').text
        
    elif div.find('span', {'class' : 'no-wrap'}):        
        return div.find('span', {'class' : 'no-wrap'}).text
    
    elif div.find(name='div', attrs={'class':'sjcl'}):
        
        div_2 = div.find(name='div', attrs={'class':'sjcl'})
        if div_2.find('div'):            
            return div_2.find('div').text
        
    else:
        return None




















