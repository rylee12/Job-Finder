import requests
import time
from bs4 import BeautifulSoup

"""
Searching category: miles, location, job words, salary?
Sort by: Rating first, Relevant location first, highest salary,
Include/Exclude: Skill, Keywords
Undecided category: Job type, education level, date posted
"""

"""
Rating star number: ratingsContent
Company name:
Number of days posted ago:
"""

def test():
    #indeed_base_url = "https://www.indeed.com/jobs?"
    based = "https://www.indeed.com"
    test_url = "https://www.indeed.com/jobs?q=computer+science&l=San+Francisco%2C+CA"

    r = requests.get(test_url)

    result = r.content

    soup = BeautifulSoup(result, 'lxml')
    #print(soup.prettify())

    m = soup.find(class_="jobsearch-SerpJobCard unifiedRow row result")
    #print(m)
    t = m.find(attrs={"data-tn-element": "jobTitle"})
    b = m.find(attrs={"data-tn-element": "companyName"})
    c = m.find(class_="ratingsContent")
    d = m.find(class_="location accessible-contrast-color-location")
    #e = m.find()
    f = m.find(class_="salaryText")
    g = m.find(class_="icl-Ratings-count")
    h = t.get("href")
    i = m.find(class_="date")
    j = m.find(class_="summary")
    #print(t["title"])
    print(t.get_text().strip())
    print(b.get_text().strip())
    print(c.get_text().strip())
    
    print(d.get_text().strip())
    print(f.get_text().strip())
    print(i.get_text().strip())
    print(j.get_text().strip())
    # when the href is retrieved, a special link combination is generated. It also leaves out the base website
    #print(h)
    print(based + str(h))


    #location


    #job_column = soup.find(id="resultsCol")

    #jobs = job_column.find_all(class_="jobsearch-SerpJobCard unifiedRow row result")
    #print(jobs)

def indeed_scraper():
    #indeed_base_url = "https://www.indeed.com/jobs?"
    based = "https://www.indeed.com"
    test_url = "https://www.indeed.com/jobs?q=computer+science&l=San+Francisco%2C+CA"

    r = requests.get(test_url)

    result = r.content

    soup = BeautifulSoup(result, 'lxml')
    
    job_column = soup.find(id="resultsCol")
    jobs = job_column.find_all(class_="jobsearch-SerpJobCard unifiedRow row result")

    job_list = []

    for item in jobs:
        title = item.find(attrs={"data-tn-element": "jobTitle"})
        if title is not None:
            title_str = ""
        else:
            title_str = ""
        
        link = title.get("href")
        company = item.find(attrs={"data-tn-element": "companyName"})
        if title is not None:
            title_str = ""
        else:
            title_str = ""

        rating = item.find(class_="ratingsContent")
        if title is not None:
            title_str = ""
        else:
            title_str = ""

        location = item.find(class_="location accessible-contrast-color-location")
        if title is not None:
            title_str = ""
        else:
            title_str = ""

        money = item.find(class_="salaryText")
        if title is not None:
            title_str = ""
        else:
            title_str = ""

        date = item.find(class_="date")
        if title is not None:
            title_str = ""
        else:
            title_str = ""

        summary = item.find(class_="summary")
        if title is not None:
            title_str = ""
        else:
            title_str = ""

#test()
indeed_scraper()
