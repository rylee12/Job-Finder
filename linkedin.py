# Do I need requests module?
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlencode
from time import sleep

PATH = "C:\Program Files (x86)\chromedriver.exe"
# Website: https://www.whatismybrowser.com/detect/what-is-my-user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"

def any_string(str_to_check, word_list):
    return any(x in str_to_check for x in word_list)

# might do something with this later
def all_string(str_to_check, word_list):
    return all(x in str_to_check for x in word_list)

def main1():
    options = Options()
    # if headless option is giving you errors that make the program break, disable it
    #options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36")
    driver = webdriver.Chrome(options=options, executable_path=PATH)

    test_url = "https://www.linkedin.com/jobs/search/?f_CF=f_WRA&geoId=90000084&keywords=engineer&location=San%20Francisco%20Bay%20Area"
    test_url2 = "https://www.linkedin.com/jobs/search/?geoId=90000084&keywords=summer%20internship%20computer%20science&location=San%20Francisco%20Bay%20Area"
    login_url = "https://www.linkedin.com/login"

    # list to hold job info
    job_list = []

    # lists to hold words to parse for
    # lower-case or not?
    exclude_list = ["chicken", "computer", "science", "meat", "internship"]
    include_list = ["python"]

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

    driver.get(test_url2)
    # this is to allow the page to load in. The number of seconds depends on loading speed and internet speed
    sleep(6)
    # scrolling down is needed to get all the posts
    elem = driver.find_element_by_class_name("jobs-search-results")
    # how much you should scroll by depends on window size and monitor size
    # 100 is half a post, 400 = 2.5 posts, 150 is nearly the post, 170 is ~exactly the post length
    for i in range(1, 8):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 500", elem)
        #print(i)
        # should make it a chance to wait a couple seconds to throw off anti-webscraping
        sleep(1)

    driver.execute_script("arguments[0].scrollTop = 0", elem)

    """
    for i in range(2, 4):
        xpath = f"/html/body/div[7]/div[3]/div[3]/div/div/section[1]/div/div/section[2]/div/ul/li[{i}]/button"
        page_button = driver.find_element_by_xpath(xpath)
        page_button.click()
        sleep(2)
    """
    
    soup = BeautifulSoup(driver.page_source, "lxml")
    job_box = soup.find(class_="jobs-search-results")
    jobs = job_box.find_all(class_="jobs-search-results__list-item occludable-update p0 relative ember-view")
    print(len(jobs))

    # could reset with the page loop?
    j = 1

    for item in jobs:
        # left-hand side
        title = item.find(class_="disabled ember-view job-card-container__link job-card-list__title")
        title_s = title.text.strip()
        #print(title.text.strip())
        #company = item.find(class_="job-card-container__link job-card-container__company-name ember-view")
        #print(company.text.strip())
        # company can be none
        """
        a = ""
        location = item.find(class_="artdeco-entity-lockup__caption ember-view")
        for city in location.find_all('li'):
            #print(text.get_text())
            a += city.get_text().strip()
            a += ' '
        print(a)
        
        b = ""
        salary = item.find(class_="mt1 t-sans t-12 t-black--light t-normal t-roman artdeco-entity-lockup__metadata ember-view")
        if salary is not None:
            for money in salary.find_all('li'):
                b += money.get_text().strip()
                b += ' '
            print(b)
        else:
            b = ""
        """
        #time_posted = item.find(class_="job-card-container__listed-time job-card-container__footer-item ")
        # https://stackoverflow.com/questions/2957013/beautifulsoup-just-get-inside-of-a-tag-no-matter-how-many-enclosing-tags-there
        # salary and location have the same li class. Are the div classes the same and static?
    
        # right-hand side
        # click on element to load the section in
        xpost = f"/html/body/div[7]/div[3]/div[3]/div/div/section[1]/div/div/ul/li[{j}]"
        #/html/body/div[{j}], j can either be 7 or 8, need to create case for it
        j += 1
        post_bt = driver.find_element_by_xpath(xpost)
        post_bt.click()
        sleep(1)

        # after clicking, refreshes bs4 object to include the new right-hand post
        soup = BeautifulSoup(driver.page_source, "lxml")
        # it turns out the clicking scrolls down for you
        # do I need to scroll down the enlarged posts on right?
        # get the link for the apply button as well?

        # seems that the essential is inside a span tag
        right = soup.find(class_="jobs-search__right-rail")
        # jobs-box__html-content jobs-description-content__text t-14 t-normal" id="job-details
        jlp = right.find(class_="jobs-box__html-content jobs-description-content__text t-14 t-normal")
        rlp = jlp.find("span")
        summary = rlp.get_text().strip().lower()
        #print(summary)

        if any_string(summary, example_list) == True:
            print("skip")
            continue
        
        print(title.text.strip())
        
        """
        type_ = []
        info_ = []
        right = soup.find(class_="jobs-search__right-rail")
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
        
        print(type_)
        print(info_)
        """
        
    
        # store info type and info text in 2 separate lists, then just index them
        #job_dict = {
        #    "title": title_s
        #}
        #job_list.append(job_dict)

    sleep(7)


    driver.quit()

main1()