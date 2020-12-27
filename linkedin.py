# Program: Linkedin Job Web Scraper
# Coder: Ryan Lee

# The runtime of the program heavily depends on internet speed (Without random sleep)
# Search for 25 posts with no filters and lxml: -- 105.98418307304382 seconds --
# Search for 25 posts with filters worst case and html.parser: -- 110.15115284919739 seconds --
# Worst case: -- 253.9741711616516 seconds -- ~ 4 minutes and 14 seconds
# Best case: -- 86.88530778884888 seconds -- ~ 1 minute and 17 seconds
# bs4: -- 88.42373275756836 seconds --, -- 86.02305293083191 seconds --, -- 86.36049270629883 seconds --
# sel: -- 89.06480884552002 seconds --, -- 88.26653218269348 seconds --, -- 86.59301114082336 seconds --

# https://selenium-python.readthedocs.io/api.html
# Chapter 7.2, has ways to move the mouse, could use to fool the website

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep, time
import pandas as pd
import random

PATH = "C:\Program Files (x86)\chromedriver.exe"
# Website: https://www.whatismybrowser.com/detect/what-is-my-user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"

def any_string(str_to_check, word_list):
    return any(x in str_to_check for x in word_list)

# might do something with this later
def all_string(str_to_check, word_list):
    return all(x in str_to_check for x in word_list)

def shorten_url(link):
    # could pass driver to shorten code
    options = Options()
    # if headless option is giving you errors that make the program break, disable it
    #options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--incognito')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36")
    dealer = webdriver.Chrome(options=options, executable_path=PATH)

    tiny_url = "https://tinyurl.com/"
    dealer.get(tiny_url)

    try:
        # enter the link into the url converter
        url_form = dealer.find_element_by_id('url')
        url_form.clear()
        url_form.send_keys(link)

        url_button = dealer.find_element_by_xpath('//*[@id="f"]/input[3]')
        url_button.click()

        # can use selenium to grab the results instead
        # class_="indent" will search for all classes with the word "indent" it, so I need to use find_all and reference the list element
        soup = BeautifulSoup(dealer.page_source, "html.parser")
        href = soup.find_all(class_="indent")
        a = href[1]
        b = a.find("b")
        answer = b.get_text().strip()
    except:
        answer = link

    dealer.quit()

    return answer

def main1(startPage, endPage, create_csv, shorten_link, search_url):
    #u = time()
    if startPage > endPage or startPage <= 0 or endPage <= 0:
        print("Error: pages inputted are not correct")
        exit()
    
    options = Options()
    # if headless option is giving you errors that make the program break, disable it
    #options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--incognito')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36")
    driver = webdriver.Chrome(options=options, executable_path=PATH)

    test_url = "https://www.linkedin.com/jobs/search/?f_CF=f_WRA&geoId=90000084&keywords=engineer&location=San%20Francisco%20Bay%20Area"
    test_url2 = "https://www.linkedin.com/jobs/search/?geoId=90000084&keywords=summer%20internship%20computer%20science&location=San%20Francisco%20Bay%20Area"

    login_url = "https://www.linkedin.com/login"

    # list to hold job info
    job_list = []

    # Variable to hold number of posts excluded/included
    count = 0
    skips = 0

    # lists to hold keywords to search for
    # lower-case or not? move it into a parameter?
    include_list = []
    exclude_list = []

    driver.get(login_url)

    # enter username and password
    # Warning: Do not leave your username and password. Insert only when needed.
    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys("<enter username here>")

    password = driver.find_element_by_id("password")
    password.clear()
    password.send_keys("<enter password here>")

    # click the login button
    login_form = driver.find_element_by_xpath("//*[@id='app__container']/main/div[2]/form/div[3]/button")
    login_form.click()

    driver.get(search_url)
    # Let the page load in. Change the number based on internet speed
    driver.implicitly_wait(5)
    sleep(random.randrange(2, 5))
    sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    maxPage = soup.find_all(class_="artdeco-pagination__indicator")
    print(maxPage)
    #maxPage_text = maxPage[-1].get_text().strip()
    #print(maxPage_text)

    # searches pages startPage to endPage(endPage included)
    for i in range(startPage, endPage + 1):
        # Noticed that the xpaths can differ, but is usually the first option
        try:
            xpath = f"/html/body/div[7]/div[3]/div[3]/div/div/section[1]/div/div/section[2]/div/ul/li[{i}]/button"
            page_button = driver.find_element_by_xpath(xpath)
            page_button.click()
        except:
            xpath = f"/html/body/div[8]/div[3]/div[3]/div/div/section[1]/div/div/section[2]/div/ul/li[{i}]/button"
            page_button = driver.find_element_by_xpath(xpath)
            page_button.click()            

        driver.implicitly_wait(5)   
        sleep(random.randrange(2, 5))
        sleep(2)

        elem = driver.find_element_by_class_name("jobs-search-results")
        # needed at the start of the program if you start at page 1
        driver.execute_script("arguments[0].scrollTop = 0", elem)

        # scrolling down is needed to get all the posts
        # how much you should scroll by depends on window size and monitor size
        # 100 is half a post, 400 = 2.5 posts, 150 is nearly the post, 170 is ~exactly the post length
        for k in range(1, 8):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 500", elem)
            # let the posts in the column load in after scrolling
            sleep(random.randrange(2, 4))
            #sleep(2)

        driver.execute_script("arguments[0].scrollTop = 0", elem)

        # get the beautifulsoup objects for the post list
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_box = soup.find(class_="jobs-search-results")
        jobs = job_box.find_all(class_="jobs-search-results__list-item occludable-update p0 relative ember-view")
        #print(len(jobs))

        # part of xpath for selenium to click on posts
        j = 1

        for item in jobs:
            # right-hand side
            # click on element to load the section in
            # Noticed that the xpaths can differ, but is usually the first option
            try:
                xpost = f"/html/body/div[7]/div[3]/div[3]/div/div/section[1]/div/div/ul/li[{j}]"
                post_bt = driver.find_element_by_xpath(xpost)
                post_bt.click()
            except:
                xpost = f"/html/body/div[8]/div[3]/div[3]/div/div/section[1]/div/div/ul/li[{j}]"
                post_bt = driver.find_element_by_xpath(xpost)
                post_bt.click()
            
            j += 1

            # let the post load in
            sleep(random.randrange(2, 4))
            #sleep(2)

            # after clicking, refreshes bs4 object to include the new right-hand post
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # it turns out the clicking scrolls down for you

            # all the text is inside a span tag
            right = soup.find(class_="jobs-search__right-rail")
            # jobs-box__html-content jobs-description-content__text t-14 t-normal" id="job-details
            jlp = right.find(class_="jobs-box__html-content jobs-description-content__text t-14 t-normal")
            rlp = jlp.find("span")
            summary = rlp.text.replace('\n', '').strip()

            if len(exclude_list) != 0 and any_string(summary, exclude_list) == True:
                skips += 1
                continue
            
            if len(include_list) != 0 and any_string(summary, include_list) == False:
                skips += 1
                continue
            
            chance2 = random.randrange(1, 3)
            if chance2 == 1:
                sleep(random.randrange(3, 6))
            

            # left-hand side
            title = item.find(class_="disabled ember-view job-card-container__link job-card-list__title")
            titl = title.get_text().strip()

            # linkedin page or company page?
            href = title.get("href")
            link = f"https://www.linkedin.com{href}"
            
            # don't think company can be none
            company = item.find(class_="job-card-container__link job-card-container__company-name ember-view")
            comp = company.get_text().strip() 

            # a is location variable, b is salary variable
            a = ""
            b = ""
            location = item.find(class_="artdeco-entity-lockup__caption ember-view")
            if location is not None:
                for city in location.find_all('li'):
                    a += city.get_text().strip()
                    a += ' '
            else:
                a = "None"

            salary = item.find(class_="mt1 t-sans t-12 t-black--light t-normal t-roman artdeco-entity-lockup__metadata ember-view")
            if salary is not None:
                for money in salary.find_all('li'):
                    b += money.get_text().strip()
                    b += ' '
            else:
                b = "None"
            
            time_posted = item.find(class_="job-card-container__listed-time job-card-container__footer-item")
            if time_posted is not None:
                ptime = time_posted.get_text().strip()
            else:
                ptime = "None"
            
            # lists to hold the job summary stuff
            type_ = []
            info_ = []
            details = right.find_all(class_="jobs-box__group")

            for im in details:
                abb = im.find(class_="t-14 t-bold")
                type_.append(abb.get_text().strip())
                imm = im.find(class_="t-14 mb3")
                if imm is None:
                    imm = im.find_all(class_="jobs-description-details__list-item t-14")
                    yum = ""
                    for word in imm:
                        yum += word.get_text().strip()
                        yum += " "
                    info_.append(yum)
                else:
                    info_.append(imm.get_text().strip())

            # shortens the original url into a tinyurl
            if shorten_link == True:
                link = shorten_url(link)
            
            count += 1

            # store info type and info text in 2 separate lists, then just index them
            job_dict = {
                "Title": titl,
                "Company": comp,
                "Location": a,
                "Salary": b,
                "Time": ptime,
                "Job_Info": type_,
                "Job_Text": info_,
                "Link": link
            }
            
            job_list.append(job_dict)

    fd = pd.DataFrame(columns=["Title", "Company", "Location", "Salary", "Time", "Job_Info", "Job_Text", "Link"])
    # Job Info:
    # Job Text: corresponds

    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
 
    # add list to dataframe
    fd = pd.DataFrame(job_list)
    print(fd)

    if create_csv == True:
        fd.to_csv("linkedin_jobs.csv", index=False)

    #print_lists(job_list)
    print("Number of posts included: " + str(count))
    print("Number of posts excluded: " + str(skips))

    #print("-- %s seconds --" % (time() - u))

    driver.quit()

# main1(startPage, endPage, create_csv)
# startPage: page to start the job search from
# endPage: page to end the job search at (results from that page included)
# create_csv: creates a csv file with the information obtained. True = create csv; False = do not create csv
# shorten_link: shortens the url to linkedin job page. True = shorten link; False = do not shorten
# search_url: the url to parse jobs for. Prepare in advance
# Note: disabling shortening will cut time of program in half. Suggest to disable when creating a csv file.
search_url = "https://www.linkedin.com/jobs/search/?geoId=90000084&keywords=summer%20internship%20computer%20science&location=San%20Francisco%20Bay%20Area"
main1(1, 1, True, False, search_url)