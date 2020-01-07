import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://www.indeed.com/jobs?q=python&l=United+States&limit={LIMIT}'

def extract_indeed_pages():
    # 'certificate verify failed' 발생시 verify=False 추가
    resul = requests.get(URL, verify=False)
    soup = BeautifulSoup(resul.text, 'html.parser')
    pagination = soup.find('div', {'class':'pagination'})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page

def extract_job(html):
    title = html.find('div', {'class':'title'}).find('a')['title']
    company = html.find('span', {'class': 'company'})
    company_anchor = company.find('a')
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = html.find('div', {'class':'recJobLoc'})['data-rc-loc']
    print(location)
    return {'title': title, 'company': company, 'location': location}

def extract_indeed_jobs(last_page):
    jobs = []
    resul = requests.get(f"{URL}&start={0*LIMIT}", verify=False)
    soup = BeautifulSoup(resul.text, 'html.parser')
    results = soup.find_all('div', {'class':'jobsearch-SerpJobCard'})
    for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs

'''
def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        resul = requests.get(f"{URL}&start={page*LIMIT}", verify=False)
        soup = BeautifulSoup(resul.text, 'html.parser')
        results = soup.find_all('div', {'class':'jobsearch-SerpJobCard'})
        print(results)
    return jobs
'''