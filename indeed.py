from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

PATH = "C:\Program Files (x86)\chromedriver.exe"

# Credit to this video: https://www.youtube.com/watch?v=QiD1lbM-utk&ab_channel=CodeHeroku
# The code to grab the html using selenium (job.get_attribute('innerHTML')) was extremely helpful and
# to close the pop-up

def any_string(str_to_check, word_list):
    return any(x in str_to_check for x in word_list)

def indeed_scraper(startPage, endPage):
    # error handling
    if startPage > endPage or startPage < 0 or endPage < 0:
        print("Starting page cannot be greater than end page number")
        exit()
    
    # Set options for selenium
    options = Options()
    options.add_argument('--incognito')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36")
    driver = webdriver.Chrome(options=options, executable_path=PATH)
    driver.maximize_window()

    dataframe = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Rating"])

    # convert startPage and endPage to values for range()
    start = (startPage - 1) * 10
    end = endPage * 10
    print(start)
    print(end)

    # lists to hold keywords to parse for in description
    include = []
    exclude = []

    # count the number of posts counted and skipped
    skips = 0
    count = 0

    # main body
    for i in range(start, end, 10):
        driver.get("https://www.indeed.com/jobs?q=Senior+Software+Engineer&l=Philadelphia%2C+PA&start=" + str(i))
        #driver.get("https://www.indeed.com/jobs?q=engineering+python+stealth+mode&l=San+Francisco+Bay+Area%2C+CA&start=" + str(i))
        driver.implicitly_wait(6)
        sleep(2)

        all_jobs = driver.find_elements_by_class_name('jobsearch-SerpJobCard')
        print(len(all_jobs))

        for job in all_jobs:
            # beautifulsoup is a bit faster
            result_html = job.get_attribute('innerHTML')
            soup = BeautifulSoup(result_html, 'html.parser')

            # try and except requires less line, can't use .text on none object
            try:
                title = soup.find("a", class_="jobtitle").text.strip()
            except:
                title = 'None'

            try:
                location = soup.find(class_="location").text.strip()
            except:
                location = 'None'

            try:
                company = soup.find(class_="company").text.strip()
            except:
                company = 'None'

            try:
                salary = soup.find(class_="salary").text.strip()
            except:
                salary = 'None'

            try:
                rating = soup.find(class_="ratingsContent").text.strip()
            except:
                rating = 'None'

            # click on the post and remove the pop-up
            sum_div = job.find_elements_by_class_name("summary")[0]
            try:
                sum_div.click()
            except:
                close_button = driver.find_elements_by_class_name("popover-x-button-close")[0]
                close_button.click()
                sum_div.click()

            # anti-webscraping
            sleep(2)
            # grab the description which is embedded in the iframe
            try:
                seq = driver.find_element_by_tag_name('iframe')
                driver.switch_to.frame(seq)
                driver.implicitly_wait(7)
                textchat = driver.find_element_by_tag_name('body').text.replace('\n', '').strip()
                #print(textchat)
                driver.switch_to.parent_frame()

                # search for keywords
                if len(include) != 0 and any_string(textchat, include) == False:
                    skips += 1
                    continue

                if len(exclude) != 0 and any_string(textchat, exclude) == True:
                    skips += 1
                    continue
            except:
                pass

            dataframe = dataframe.append({'Title': title,
                                        'Location': location,
                                        "Company": company,
                                        "Salary": salary,
                                        "Rating": rating},
                                        ignore_index=True)
            
            count += 1

    print(dataframe)
    print("Number of skips: " + str(skips))
    print("Number of posts: " + str(count))

indeed_scraper(1, 1)
