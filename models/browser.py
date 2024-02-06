from robocorp import browser
from RPA.HTTP import HTTP
from  RPA.Browser.Selenium import WebDriverWait

from datetime import datetime, date, timedelta
from models.crawler import Crawler

import time
import random

import logging

logging.basicConfig(level=logging.INFO,
                    filename="robot.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")

class Browser:

    def __init__(self, months_qtd: int, section: str, news_user: str) -> None:

        # browser.goto(site)
        browser.configure(
            slowmo=10,
            # browser_engine='msedge',
        )

        self.site = 'https://www.nytimes.com/'

        self.page    = browser.page()
        self.crawler = Crawler()
        
        self.inputs  = {
            "months"  : months_qtd,
            "section" : section,
            "news"    : news_user
        }

        browser.goto(self.site)

        logging.info(f"access {self.page.url}")

        time.sleep(random.randint(1,5))
        
        try:
            self.page.click("button:text('Accept all')")
        except:
            print("No Cookies detected")
            logging.info("no cookies pop-up detected")
            pass

        self.search(self.inputs["news"], self.inputs["months"], self.inputs["section"])

        logging.info(f"Order by Newest")

        self.page.select_option("data-testid=SearchForm-sortBy", "Sort by Newest")
        
        """Click to get all news"""
        
        # while True:
        #     try:
        #         self.page.click("button:text('Show More')")
        #     except:
        #         print("No More News on Page")
                # break
        
        print(self.page.url)

        self.news = self.crawler.soup(self.page.url)


    def search(self, news: str, month:int, section: str) -> bool:

        """Serch on New York Times for user's news"""

        logging.info(f"Searching for {news}")

        time.sleep(random.randint(1,5))
        self.page.click("data-testid=search-button")
        time.sleep(random.randint(1,5))
        self.page.fill(".css-1u4s13l", "oi")
        time.sleep(random.randint(1,5))
        self.page.click("button:text('Go')")
        
        time.sleep(random.randint(1,3))

        '''
        Checking Copywrite Page
        '''

        while True:
            if self.copy_treatment():

                logging.info("Copywrite page detected. Restarting the process")

                browser.goto(self.site)
                self.search(self.inputs["news"], self.inputs["months"], self.inputs["section"])
            else:
                break

        self.filter_section(section)
        self.filter_time(month)

    def copy_treatment(self) -> bool:

        """Copywrite Treatments"""

        copy = self.page.url
        if 'Copy' in copy:
            return True
        else:
            return False
            
    def filter_time(self, month: int) -> None:

        """Filter by month quantities"""

        logging.info("Filter by months")

        self.page.click("data-testid=search-date-dropdown-a")
        self.page.click("button:text('Specific Dates')")

        if month == 0 or month == 1:
            date_user = datetime.now()
        else:
            date_user = datetime.now() - timedelta(days=30*month)

        self.page.fill(f"#startDate", f"{date_user.month}/01/{date_user.year}")

        time.sleep(random.randint(1,4))

        if date_user.month == 2:

            if datetime.now().year // 4 != 0:
                self.page.fill("#endDate", f"28/{date_user.month}/28/2024")
            else:
                self.page.fill("#endDate", f"29/{date_user.month}/29/2024")

        elif date_user.month in [1,3,5,7,8,10,12]:
            self.page.fill("#endDate", f"{date_user.month}/31/2024")

        else:
            self.page.fill("#endDate", f"{date_user.month}/30/2024")
        
        time.sleep(1)

        self.page.click("data-testid=search-date-dropdown-a")
        self.page.click("data-testid=SearchForm-sortBy")

        time.sleep(random.randint(10,15))

    def filter_section(self, section: str):

        """Filter by section"""

        logging.info("Filter by section")

        if section not in ['Any', 'Arts', 'Books', 'Business', 'New York', 'Opinion', 'Sports', 'Travel', 'U.S.', 'World']:
            print("Invalid Section Error!")
            pass
        else:
            self.page.click("data-testid=search-multiselect-button")
            self.page.click(f"span:text('{section}')")
            self.page.click("data-testid=search-multiselect-button")