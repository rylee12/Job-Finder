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

def main1():
    options = Options()
    # if headless option is giving you errors that make the program break, disable it
    #options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36")
    driver = webdriver.Chrome(options=options, executable_path=PATH)

    test_url2 = "https://www.linkedin.com/jobs/search/?geoId=90000084&keywords=summer%20internship%20computer%20science&location=San%20Francisco%20Bay%20Area"
    login_url = "https://www.linkedin.com/login"
    # linkedin buttons generate random number, but if ur at current page, then next page is current id + 2, next after that is previous id + 3

    # lists to hold job info
    job_list = []

    driver.get(login_url)

    # login process
    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys("<insert email here>")

    password = driver.find_element_by_id("password")
    password.clear()
    password.send_keys("<insert password here>")

    # xpath: //*[@id="app__container"]/main/div[2]/form/div[3]/button
    login_form = driver.find_element_by_xpath("//*[@id='app__container']/main/div[2]/form/div[3]/button")
    login_form.click()

    driver.get(test_url2)
    # this is to allow the page to load in
    sleep(7)
    # scrolling down not needed
    elem = driver.find_element_by_class_name("jobs-search-results")
    #driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", elem)
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 170", elem)
    # 100 is half a post, 400 = 2.5 posts, 150 is nearly the post, 170 is ~exactly the post length
    sleep(10)
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 170", elem)
    sleep(10)

    """
    for i in range(2, 4):
        xpath = f"/html/body/div[7]/div[3]/div[3]/div/div/section[1]/div/div/section[2]/div/ul/li[{i}]/button"
        page_button = driver.find_element_by_xpath(xpath)
        page_button.click()
        sleep(4)
    """
    
    soup = BeautifulSoup(driver.page_source, "lxml")
    job_box = soup.find(class_="jobs-search-results")
    jobs = job_box.find_all(class_="jobs-search-results__list-item occludable-update p0 relative ember-view")

    for item in jobs:
        # left-hand side
        title = item.find(class_="disabled ember-view job-card-container__link job-card-list__title")
        print(title.text.strip())
        company = item.find(class_="job-card-container__link job-card-container__company-name ember-view")
        print(company.text.strip())
        # company can be none
        #location = item.find(class_="job-card-container__metadata-item")
        # can location be none?
        #time_posted = item.find(class_="job-card-container__listed-time job-card-container__footer-item ")
        # https://stackoverflow.com/questions/2957013/beautifulsoup-just-get-inside-of-a-tag-no-matter-how-many-enclosing-tags-there
        # salary and location have the same li class. Are the div classes the same and static?
    """
        # right-hand side
        # click on element to load the section in
        # get the link for the apply button as well?
        right = .find(class_="jobs-search__right-rail")
        description = .find(class_="jobs-description-details pt4")
        details = .find_all(class_="jobs-box__group")
        # loop through details (decide on which structure)
            info_type = .find(class_="t-14 t-bold")
            info_text = .find(class_="t-14 mb3")
        
    """

    sleep(10)


    driver.quit()

main1()