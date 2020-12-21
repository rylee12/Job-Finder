# Program: Linkedin Job Web Scraper
# Coder: Ryan Lee

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
#from urllib.parse import urlencode
from time import sleep
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
    options = Options()
    # if headless option is giving you errors that make the program break, disable it
    #options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--incognito')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36")
    dealer = webdriver.Chrome(options=options, executable_path=PATH)

    tiny_url = "https://tinyurl.com/"
    dealer.get(tiny_url)

    # enter the link into the url converter
    url_form = dealer.find_element_by_id('url')
    url_form.clear()
    url_form.send_keys(link)

    url_button = dealer.find_element_by_xpath('//*[@id="f"]/input[3]')
    url_button.click()

    # class_="indent" will search for all classes with the word "indent" it, so I need to use find_all and reference the list element
    soup = BeautifulSoup(dealer.page_source, "lxml")
    href = soup.find_all(class_="indent")
    a = href[1]
    b = a.find("b")
    answer = b.get_text().strip()

    dealer.quit()

    return answer

def print_lists(list1):
    for thing in list1:
        print(thing)
        print()

def main1():
    options = Options()
    # if headless option is giving you errors that make the program break, disable it
    #options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--incognito')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36")
    driver = webdriver.Chrome(options=options, executable_path=PATH)

    test_url = "https://www.linkedin.com/jobs/search/?f_CF=f_WRA&geoId=90000084&keywords=engineer&location=San%20Francisco%20Bay%20Area"
    test_url2 = "https://www.linkedin.com/jobs/search/?geoId=90000084&keywords=summer%20internship%20computer%20science&location=San%20Francisco%20Bay%20Area"

    search_url = "https://www.linkedin.com/jobs/search/?geoId=90000084&keywords=summer%20internship%20computer%20science&location=San%20Francisco%20Bay%20Area"
    login_url = "https://www.linkedin.com/login"

    # list to hold job info
    job_list = []

    # Variable to hold number of posts excluded/included
    count = 0
    skips = 0

    # lists to hold words to parse for
    # lower-case or not?
    include_list = ["python"]
    exclude_list = ["chicken"]

    # data structure:
    # make a dictionary containing each post information
    # Note: make sure to check post for the words first

    driver.get(login_url)

    # login process
    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys("<insert username>")

    password = driver.find_element_by_id("password")
    password.clear()
    password.send_keys("<insert password>")

    # xpath: //*[@id="app__container"]/main/div[2]/form/div[3]/button
    login_form = driver.find_element_by_xpath("//*[@id='app__container']/main/div[2]/form/div[3]/button")
    login_form.click()

    driver.get(search_url)
    # this is to allow the page to load in. The number of seconds depends on loading speed and internet speed
    sleep(5)

    # To search from pages i to j (j included), replace the numbers in range() with i and j + 1
    for i in range(1, 2):
        xpath = f"/html/body/div[7]/div[3]/div[3]/div/div/section[1]/div/div/section[2]/div/ul/li[{i}]/button"
        page_button = driver.find_element_by_xpath(xpath)
        page_button.click()
        sleep(5)

        elem = driver.find_element_by_class_name("jobs-search-results")
        # needed at the start of the program if you start at page 1
        driver.execute_script("arguments[0].scrollTop = 0", elem)

        # scrolling down is needed to get all the posts
        # how much you should scroll by depends on window size and monitor size
        # 100 is half a post, 400 = 2.5 posts, 150 is nearly the post, 170 is ~exactly the post length
        for k in range(1, 8):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 500", elem)
            # should make it a chance to wait a couple seconds to throw off anti-webscraping
            chance = random.randrange(1, 3)
            if chance != 1:
                sleep(random.randrange(1, 3))

        sleep(1)
        driver.execute_script("arguments[0].scrollTop = 0", elem)

        # get the beautifulsoup objects for the post list
        soup = BeautifulSoup(driver.page_source, "lxml")
        job_box = soup.find(class_="jobs-search-results")
        jobs = job_box.find_all(class_="jobs-search-results__list-item occludable-update p0 relative ember-view")
        print(len(jobs))

        # part of xpath for selenium to click on posts
        j = 1

        for item in jobs:
            # right-hand side
            # click on element to load the section in
            xpost = f"/html/body/div[7]/div[3]/div[3]/div/div/section[1]/div/div/ul/li[{j}]"
            j += 1
            post_bt = driver.find_element_by_xpath(xpost)
            post_bt.click()
            sleep(random.randrange(1, 3))

            # after clicking, refreshes bs4 object to include the new right-hand post
            soup = BeautifulSoup(driver.page_source, "lxml")
            # it turns out the clicking scrolls down for you

            # all the text is inside a span tag
            right = soup.find(class_="jobs-search__right-rail")
            # jobs-box__html-content jobs-description-content__text t-14 t-normal" id="job-details
            jlp = right.find(class_="jobs-box__html-content jobs-description-content__text t-14 t-normal")
            rlp = jlp.find("span")
            summary = rlp.get_text().strip().lower()
            #print(summary)

            if exclude_list != 0 and any_string(summary, exclude_list) == True:
                #print("skip")
                skips += 1
                continue
            
            if include_list != 0 and any_string(summary, include_list) == False:
                #print("skip")
                skips += 1
                continue

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
            
            #print(type_)
            #print(info_)

            # need to shorten the original url
            tiny_link = shorten_url(link)
            
            count += 1

            # store info type and info text in 2 separate lists, then just index them
            job_dict = {
                "title": titl,
                "company": comp,
                "location": a,
                "salary": b,
                "time": ptime,
                "job_info": type_,
                "job_text": info_,
                "link": tiny_link
            }
            
            job_list.append(job_dict)

    print_lists(job_list)
    print("Number of posts included: " + str(count))
    print("Number of posts excluded: " + str(skips))
    sleep(4)

    driver.quit()

main1()