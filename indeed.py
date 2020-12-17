import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlencode

"""
Features:
1. Look for start-ups
2. Sort stuff based on certain critera i.e. keywords, salary. Include/exclude
"""

"""
Searching category: miles, location, job words, salary?
Sort by: Rating first, Relevant location first, highest salary,
Include/Exclude: Skill, Keywords
Undecided category: Job type, education level, date posted
"""

"""
q = keywords to search for
l = location
radius = distance within location to search
fromage = date posted
jt = job type
"""

search_dict = {
    "q": "computer science",
    "l": "San Francisco, CA"
}

def indeed_scraper():
    #test_url = "https://www.indeed.com/jobs?q=computer+science&l=San+Francisco%2C+CA"
    #search_url = test_url
    page = "0"

    encoded_query = urlencode(search_dict)
    search_url = f"https://www.indeed.com/jobs?{encoded_query}"

    job_list = []
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    g = []
    h = []

    while page != "1":
        r = requests.get(search_url)

        result = r.content

        soup = BeautifulSoup(result, 'lxml')
        
        job_column = soup.find(id="resultsCol")
        jobs = job_column.find_all(class_="jobsearch-SerpJobCard unifiedRow row result")

        # get the page number to go to the next page
        t = job_column.find(attrs={"aria-current": "true"})
        page = t.text.strip()
        #print(page)
        """
        if t.text.strip() == "2":
            print("I got it!")
            break
        else:
            print("You're lousy")
            print(t.text.strip())
        """
        
        search_url = get_next(soup)
        #print(search_url)

        for item in jobs:
            #print("inner loop")

            title = item.find(attrs={"data-tn-element": "jobTitle"})
            if title is not None:
                title_txt = title.text.strip() 
            else:
                title_txt = "None"

            href = title.get("href")
            link = f"https://www.indeed.com{href}"

            company = item.find(class_="company")
            if company is not None:
                company_txt = company.text.strip()
            else:
                company_txt = "N/A"

            rating = item.find(class_="ratingsContent")
            if rating is not None:
                rating_txt = rating.text.strip()
            else:
                rating_txt = "N/A"

            location = item.find(class_="location accessible-contrast-color-location")
            if location is not None:
                location_txt = location.text.strip()
            else:
                location_txt = "None"

            money = item.find(class_="salaryText")
            if money is not None:
                money_txt = money.text.strip()
            else:
                money_txt = "N/A"

            date = item.find(class_="date")
            if date is not None:
                date_txt = date.text.strip()
            else:
                date_txt = "N/A"

            summary = item.find(class_="summary")
            if summary is not None:
                summary_txt = summary.text.strip()
            else:
                summary_txt = "N/A"

            a.append(title_txt)
            b.append(company_txt)
            c.append(rating_txt)
            d.append(location_txt)
            e.append(money_txt)
            f.append(date_txt)
            g.append(summary_txt)
            h.append(link)
            """
            job_dict = {
                "title": title_txt,
                "company": company_txt,
                "rating": rating_txt,
                "location": location_txt,
                "money": money_txt,
                "date": date_txt,
                "summary": summary_txt,
                "href": link,
            }

            job_list.append(job_dict)
            """


    print("debug the pandas")    
    #print(pd.get_option("display.max_columns"))
    #pd.set_option('display.max_columns', 0)    
    job_info = pd.DataFrame(data={'Title': a,
    'Company': b,
    'Rating': c,
    'Location': d,
    'Money': e,
    'Date': f,
    'Summary': g,
    'Href': h
    })
    print(job_info)
    #print(job_info.info())
    #print(job_info.head())
    #for elem in job_list:
    #    print(elem)
    #    print("\n")
    job_info['Summary'] = job_info['Summary'].str.replace('\n',' ')
    job_info.to_csv("job.csv", sep='\t', encoding='utf-8', index=False, header=True)
        

def test_loop():
    #indeed_base_url = "https://www.indeed.com/jobs?"
    based = "https://www.indeed.com"
    test_url = "https://www.indeed.com/jobs?q=computer+science&l=San+Francisco%2C+CA"
    page = "0"

    url_loop = test_url
    
    while page != "3":
        r = requests.get(url_loop)

        result = r.content

        soup = BeautifulSoup(result, 'lxml')
        
        job_column = soup.find(id="resultsCol")
        jobs = job_column.find_all(class_="jobsearch-SerpJobCard unifiedRow row result")

        for item in jobs:
            title = item.find(attrs={"data-tn-element": "jobTitle"})
            if title is not None:
                print(title.text.strip())

        # need to move this up
        t = job_column.find(attrs={"aria-current": "true"})
        if t.text.strip() == "3":
            print("I got it!")
            break
        else:
            print("You're lousy")
        
        url_loop = get_next(soup)
        print(url_loop)

def get_next(soup):
    next_tm = soup.find(attrs={"aria-label": "Next"})
    # Check to see if there is another page or not
    if next_tm is not None:
        return f"https://www.indeed.com{next_tm['href']}"
    return ""    


#test()
#test_loop()
indeed_scraper()
