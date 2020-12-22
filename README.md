# Job-Finder
**Disclosure:**
Some websites do not approve of webscraping and may IP ban you if they detect it, linkedin included. Please use at your own risk. Do not use my program, modified or not, to webscrape private information.

**Installation:**
This program uses python, so use the terminal to pip install the packages. Website to find the packages: https://pypi.org/
1. Installing BeautifulSoup
- In the terminal, type: pip install beautifulsoup4
2. Installing Selenium
- In the terminal, type: pip install selenium
3. Installing Selenium Chromedriver
- This program uses the selenium webdriver for the google chrome browser
- Download website: https://sites.google.com/a/chromium.org/chromedriver/downloads
- Choose the version of chromedriver that corresponds to your google chrome version. To check the version, click on the 3-vertical dots
symbol on the top-right corner, hover over "Help" with your mouse, and then click on "About Google Chrome" to find the version.
- Once you have downloaded chromedriver, I suggest moving it to a new location from the zip file. Then copy the address i.e. location of
the file and replace the PATH variable in the program with the new address of your chromedriver.

**How to Use**
LinkedIn Job Scraper:
- To search for a certain job, replace the search_url with the url you want to search.
- To modify which pages are searched, replace the values in the range() function.
- To run LinkedIn Job Scraper, open up the terminal, go to the file's location, and then type "python linkedin.py" to run the linkedin job scraper.
