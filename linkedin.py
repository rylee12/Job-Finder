# Program: Linkedin Job Web Scraper
# Coder: Ryan Lee	# Coder: Ryan Lee


# The runtime of the program heavily depends on internet speed (Without random sleep)
# Search for 25 posts with no filters and lxml: -- 105.98418307304382 seconds --
# Search for 25 posts with filters worst case and html.parser: -- 110.15115284919739 seconds --
# Worst case: -- 253.9741711616516 seconds -- ~ 4 minutes and 14 seconds
# Best case: -- 86.88530778884888 seconds -- ~ 1 minute and 17 seconds
# bs4: -- 88.42373275756836 seconds --, -- 86.02305293083191 seconds --, -- 86.36049270629883 seconds --
# sel: -- 89.06480884552002 seconds --, -- 88.26653218269348 seconds --, -- 86.59301114082336 seconds --

# https://selenium-python.readthedocs.io/api.html
# Chapter 7.2, has ways to move the mouse, could use to fool the website

from bs4 import BeautifulSoup	from bs4 import BeautifulSoup
from selenium import webdriver	from selenium import webdriver
from selenium.webdriver.common.keys import Keys	
from selenium.webdriver.chrome.options import Options	from selenium.webdriver.chrome.options import Options
#from urllib.parse import urlencode	from time import sleep, time
from time import sleep	import pandas as pd
import random	import random


PATH = "C:\Program Files (x86)\chromedriver.exe"	PATH = "C:\Program Files (x86)\chromedriver.exe"
@@ -21,6 +31,7 @@ def all_string(str_to_check, word_list):
    return all(x in str_to_check for x in word_list)	    return all(x in str_to_check for x in word_list)


def shorten_url(link):	def shorten_url(link):
    # could pass driver to shorten code
    options = Options()	    options = Options()
    # if headless option is giving you errors that make the program break, disable it	    # if headless option is giving you errors that make the program break, disable it
    #options.add_argument("--headless")	    #options.add_argument("--headless")
@@ -32,31 +43,35 @@ def shorten_url(link):
    tiny_url = "https://tinyurl.com/"	    tiny_url = "https://tinyurl.com/"
    dealer.get(tiny_url)	    dealer.get(tiny_url)


    # enter the link into the url converter	    try:
    url_form = dealer.find_element_by_id('url')	        # enter the link into the url converter
    url_form.clear()	        url_form = dealer.find_element_by_id('url')
    url_form.send_keys(link)	        url_form.clear()

        url_form.send_keys(link)
    url_button = dealer.find_element_by_xpath('//*[@id="f"]/input[3]')	
    url_button.click()	        url_button = dealer.find_element_by_xpath('//*[@id="f"]/input[3]')

        url_button.click()
    # class_="indent" will search for all classes with the word "indent" it, so I need to use find_all and reference the list element	
    soup = BeautifulSoup(dealer.page_source, "lxml")	        # can use selenium to grab the results instead
    href = soup.find_all(class_="indent")	        # class_="indent" will search for all classes with the word "indent" it, so I need to use find_all and reference the list element
    a = href[1]	        soup = BeautifulSoup(dealer.page_source, "html.parser")
    b = a.find("b")	        href = soup.find_all(class_="indent")
    answer = b.get_text().strip()	        a = href[1]
        b = a.find("b")
        answer = b.get_text().strip()
    except:
        answer = link


    dealer.quit()	    dealer.quit()


    return answer	    return answer


def print_lists(list1):	def main1(startPage, endPage, create_csv, shorten_link, search_url):
    for thing in list1:	    #u = time()
        print(thing)	    if startPage > endPage or startPage <= 0 or endPage <= 0:
        print()	        print("Error: pages inputted are not correct")

        exit()
def main1():	    
    options = Options()	    options = Options()
    # if headless option is giving you errors that make the program break, disable it	    # if headless option is giving you errors that make the program break, disable it
    #options.add_argument("--headless")	    #options.add_argument("--headless")
@@ -68,7 +83,6 @@ def main1():
    test_url = "https://www.linkedin.com/jobs/search/?f_CF=f_WRA&geoId=90000084&keywords=engineer&location=San%20Francisco%20Bay%20Area"	    test_url = "https://www.linkedin.com/jobs/search/?f_CF=f_WRA&geoId=90000084&keywords=engineer&location=San%20Francisco%20Bay%20Area"
    test_url2 = "https://www.linkedin.com/jobs/search/?geoId=90000084&keywords=summer%20internship%20computer%20science&location=San%20Francisco%20Bay%20Area"	    test_url2 = "https://www.linkedin.com/jobs/search/?geoId=90000084&keywords=summer%20internship%20computer%20science&location=San%20Francisco%20Bay%20Area"


    search_url = "https://www.linkedin.com/jobs/search/?geoId=90000084&keywords=summer%20internship%20computer%20science&location=San%20Francisco%20Bay%20Area"	
    login_url = "https://www.linkedin.com/login"	    login_url = "https://www.linkedin.com/login"


    # list to hold job info	    # list to hold job info
@@ -78,40 +92,54 @@ def main1():
    count = 0	    count = 0
    skips = 0	    skips = 0


    # lists to hold words to parse for	    # lists to hold keywords to search for
    # lower-case or not?	    # lower-case or not? move it into a parameter?
    include_list = ["python"]	    include_list = []
    exclude_list = ["chicken"]	    exclude_list = []

    # data structure:	
    # make a dictionary containing each post information	
    # Note: make sure to check post for the words first	


    driver.get(login_url)	    driver.get(login_url)


    # login process	    # enter username and password
    # Warning: Do not leave your username and password. Insert only when needed.
    username = driver.find_element_by_id("username")	    username = driver.find_element_by_id("username")
    username.clear()	    username.clear()
    username.send_keys("<insert username>")	    username.send_keys("error2000noname@gmail.com")


    password = driver.find_element_by_id("password")	    password = driver.find_element_by_id("password")
    password.clear()	    password.clear()
    password.send_keys("<insert password>")	    password.send_keys("Erryumpop57")


    # xpath: //*[@id="app__container"]/main/div[2]/form/div[3]/button	    # click the login button
    login_form = driver.find_element_by_xpath("//*[@id='app__container']/main/div[2]/form/div[3]/button")	    login_form = driver.find_element_by_xpath("//*[@id='app__container']/main/div[2]/form/div[3]/button")
    login_form.click()	    login_form.click()


    driver.get(search_url)	    driver.get(search_url)
    # this is to allow the page to load in. The number of seconds depends on loading speed and internet speed	    # Let the page load in. Change the number based on internet speed
    sleep(5)	    driver.implicitly_wait(5)

    sleep(random.randrange(2, 5))
    # To search from pages i to j (j included), replace the numbers in range() with i and j + 1	    sleep(2)
    for i in range(1, 2):	
        xpath = f"/html/body/div[7]/div[3]/div[3]/div/div/section[1]/div/div/section[2]/div/ul/li[{i}]/button"	    soup = BeautifulSoup(driver.page_source, "html.parser")
        page_button = driver.find_element_by_xpath(xpath)	    maxPage = soup.find_all(class_="artdeco-pagination__indicator")
        page_button.click()	    print(maxPage)
        sleep(5)	    #maxPage_text = maxPage[-1].get_text().strip()
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


        elem = driver.find_element_by_class_name("jobs-search-results")	        elem = driver.find_element_by_class_name("jobs-search-results")
        # needed at the start of the program if you start at page 1	        # needed at the start of the program if you start at page 1
@@ -122,53 +150,63 @@ def main1():
        # 100 is half a post, 400 = 2.5 posts, 150 is nearly the post, 170 is ~exactly the post length	        # 100 is half a post, 400 = 2.5 posts, 150 is nearly the post, 170 is ~exactly the post length
        for k in range(1, 8):	        for k in range(1, 8):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 500", elem)	            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 500", elem)
            # should make it a chance to wait a couple seconds to throw off anti-webscraping	            # let the posts in the column load in after scrolling
            chance = random.randrange(1, 3)	            sleep(random.randrange(2, 4))
            if chance != 1:	            #sleep(2)
                sleep(random.randrange(1, 3))	


        sleep(1)	
        driver.execute_script("arguments[0].scrollTop = 0", elem)	        driver.execute_script("arguments[0].scrollTop = 0", elem)


        # get the beautifulsoup objects for the post list	        # get the beautifulsoup objects for the post list
        soup = BeautifulSoup(driver.page_source, "lxml")	        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_box = soup.find(class_="jobs-search-results")	        job_box = soup.find(class_="jobs-search-results")
        jobs = job_box.find_all(class_="jobs-search-results__list-item occludable-update p0 relative ember-view")	        jobs = job_box.find_all(class_="jobs-search-results__list-item occludable-update p0 relative ember-view")
        print(len(jobs))	        #print(len(jobs))


        # part of xpath for selenium to click on posts	        # part of xpath for selenium to click on posts
        j = 1	        j = 1


        for item in jobs:	        for item in jobs:
            # right-hand side	            # right-hand side
            # click on element to load the section in	            # click on element to load the section in
            xpost = f"/html/body/div[7]/div[3]/div[3]/div/div/section[1]/div/div/ul/li[{j}]"	            # Noticed that the xpaths can differ, but is usually the first option
            try:
                xpost = f"/html/body/div[7]/div[3]/div[3]/div/div/section[1]/div/div/ul/li[{j}]"
                post_bt = driver.find_element_by_xpath(xpost)
                post_bt.click()
            except:
                xpost = f"/html/body/div[8]/div[3]/div[3]/div/div/section[1]/div/div/ul/li[{j}]"
                post_bt = driver.find_element_by_xpath(xpost)
                post_bt.click()

            j += 1	            j += 1
            post_bt = driver.find_element_by_xpath(xpost)	
            post_bt.click()	            # let the post load in
            sleep(random.randrange(1, 3))	            sleep(random.randrange(2, 4))
            #sleep(2)


            # after clicking, refreshes bs4 object to include the new right-hand post	            # after clicking, refreshes bs4 object to include the new right-hand post
            soup = BeautifulSoup(driver.page_source, "lxml")	            soup = BeautifulSoup(driver.page_source, "html.parser")
            # it turns out the clicking scrolls down for you	            # it turns out the clicking scrolls down for you


            # all the text is inside a span tag	            # all the text is inside a span tag
            right = soup.find(class_="jobs-search__right-rail")	            right = soup.find(class_="jobs-search__right-rail")
            # jobs-box__html-content jobs-description-content__text t-14 t-normal" id="job-details	            # jobs-box__html-content jobs-description-content__text t-14 t-normal" id="job-details
            jlp = right.find(class_="jobs-box__html-content jobs-description-content__text t-14 t-normal")	            jlp = right.find(class_="jobs-box__html-content jobs-description-content__text t-14 t-normal")
            rlp = jlp.find("span")	            rlp = jlp.find("span")
            summary = rlp.get_text().strip().lower()	            summary = rlp.text.replace('\n', '').strip()
            #print(summary)	


            if exclude_list != 0 and any_string(summary, exclude_list) == True:	            if len(exclude_list) != 0 and any_string(summary, exclude_list) == True:
                #print("skip")	
                skips += 1	                skips += 1
                continue	                continue


            if include_list != 0 and any_string(summary, include_list) == False:	            if len(include_list) != 0 and any_string(summary, include_list) == False:
                #print("skip")	
                skips += 1	                skips += 1
                continue	                continue

            chance2 = random.randrange(1, 3)
            if chance2 == 1:
                sleep(random.randrange(3, 6))



            # left-hand side	            # left-hand side
            title = item.find(class_="disabled ember-view job-card-container__link job-card-list__title")	            title = item.find(class_="disabled ember-view job-card-container__link job-card-list__title")
@@ -225,34 +263,56 @@ def main1():
                    info_.append(yum)	                    info_.append(yum)
                else:	                else:
                    info_.append(imm.get_text().strip())	                    info_.append(imm.get_text().strip())

            #print(type_)	
            #print(info_)	


            # need to shorten the original url	            # shortens the original url into a tinyurl
            tiny_link = shorten_url(link)	            if shorten_link == True:
                link = shorten_url(link)


            count += 1	            count += 1


            # store info type and info text in 2 separate lists, then just index them	            # store info type and info text in 2 separate lists, then just index them
            job_dict = {	            job_dict = {
                "title": titl,	                "Title": titl,
                "company": comp,	                "Company": comp,
                "location": a,	                "Location": a,
                "salary": b,	                "Salary": b,
                "time": ptime,	                "Time": ptime,
                "job_info": type_,	                "Job_Info": type_,
                "job_text": info_,	                "Job_Text": info_,
                "link": tiny_link	                "Link": link
            }	            }


            job_list.append(job_dict)	            job_list.append(job_dict)


    print_lists(job_list)	    fd = pd.DataFrame(columns=["Title", "Company", "Location", "Salary", "Time", "Job_Info", "Job_Text", "Link"])
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
    print("Number of posts included: " + str(count))	    print("Number of posts included: " + str(count))
    print("Number of posts excluded: " + str(skips))	    print("Number of posts excluded: " + str(skips))
    sleep(4)	
    #print("-- %s seconds --" % (time() - u))


    driver.quit()

# startPage: page to start the job search from
# endPage: page to end the job search at (results from that page included)
# create_csv: creates a csv file with the information obtained. True = create csv; False = do not create csv
# shorten_link: shortens the url to linkedin job page. True = shorten link; False = do not shorten
# search_url: the url to parse jobs for. Prepare in advance
# Note: disabling shortening will cut time of program in half. Suggest to disable when creating a csv file.
search_url = "https://www.linkedin.com/jobs/search/?geoId=90000084&keywords=summer%20internship%20computer%20science&location=San%20Francisco%20Bay%20Area"
main1(1, 1, True, False, search_url