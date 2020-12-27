from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
from time import sleep, time
import pandas as pd
import random

PATH = "C:\Program Files (x86)\chromedriver.exe"

# Credit to this video: https://www.youtube.com/watch?v=QiD1lbM-utk&ab_channel=CodeHeroku
# The code to grab the html using selenium (job.get_attribute('innerHTML')) was extremely helpful and
# to close the pop-up

# Runtime counting (Depends on internet speed)
# Average case: -- 86.61412215232849 seconds --

def any_string(str_to_check, word_list):
    return any(x in str_to_check for x in word_list)

def indeed_scraper(startPage, endPage):
def indeed_scraper(startPage, endPage, create_csv, search_url):
    # error handling
    if startPage > endPage or startPage < 0 or endPage < 0:
        print("Starting page cannot be greater than end page number")
    #u = time()
    if startPage > endPage or startPage <= 0 or endPage <= 0:
        print("Error: pages inputted are not correct")
        exit()

    # Set options for selenium
@@ -26,13 +31,13 @@ def indeed_scraper(startPage, endPage):
    driver = webdriver.Chrome(options=options, executable_path=PATH)
    driver.maximize_window()

    dataframe = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Rating"])
    df = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Rating"])

    search_url_mod = search_url + "&start="

    # convert startPage and endPage to values for range()
    start = (startPage - 1) * 10
    end = endPage * 10
    print(start)
    print(end)

    # lists to hold keywords to parse for in description
    include = []
@@ -44,13 +49,12 @@ def indeed_scraper(startPage, endPage):

    # main body
    for i in range(start, end, 10):
        driver.get("https://www.indeed.com/jobs?q=Senior+Software+Engineer&l=Philadelphia%2C+PA&start=" + str(i))
        #driver.get("https://www.indeed.com/jobs?q=engineering+python+stealth+mode&l=San+Francisco+Bay+Area%2C+CA&start=" + str(i))
        driver.get(search_url_mod + str(i))
        driver.implicitly_wait(6)
        sleep(2)

        all_jobs = driver.find_elements_by_class_name('jobsearch-SerpJobCard')
        print(len(all_jobs))
        #print(len(all_jobs))

        for job in all_jobs:
            # beautifulsoup is a bit faster
@@ -59,7 +63,10 @@ def indeed_scraper(startPage, endPage):

            # try and except requires less line, can't use .text on none object
            try:
                title = soup.find("a", class_="jobtitle").text.strip()
                title = soup.find("a", class_="jobtitle")
                title1 = title.text.strip()
                href = title.get('href')
                link = f"https://www.indeed.com{href}"
            except:
                title = 'None'

@@ -93,14 +100,15 @@ def indeed_scraper(startPage, endPage):
                sum_div.click()

            # anti-webscraping
            sleep(2)
            sleep(random.randrange(2, 5))

            # grab the description which is embedded in the iframe
            try:
                seq = driver.find_element_by_tag_name('iframe')
                driver.switch_to.frame(seq)
                driver.implicitly_wait(7)
                sleep(2)
                textchat = driver.find_element_by_tag_name('body').text.replace('\n', '').strip()
                #print(textchat)
                driver.switch_to.parent_frame()
            except:
                pass

            sleep(random.randrange(2, 5))

            df = df.append({'Title': title1,
                            'Location': location,
                            "Company": company,
                            "Salary": salary,
                            "Rating": rating,
                            "Link": link},
                            ignore_index=True)

            count += 1

    print(df)

    if create_csv == True:
        df.to_csv("indeed_jobs.csv", index=False)

    print("Number of skips: " + str(skips))
    print("Number of posts: " + str(count))
    #print("-- %s seconds --" % (time() - u))

# indeed_scraper(startPage, endPage)
# startPage: page to start the job search from
# endPage: page to end the job search at (results from that page included)
# create_csv: creates a csv file with the information obtained. True = create csv; False = do not create csv
# search_url: the url to parse jobs for. Prepare in advance
# Note: links are cut off in terminal due to length issues. Enable create_csv to get complete link.
# add salary option?
search_url = "https://www.indeed.com/jobs?q=engineering&l=San+Francisco+Bay+Area%2C+CA"
indeed_scraper(1, 1, True, search_url)