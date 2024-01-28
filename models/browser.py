from robocorp import browser

from RPA.HTTP import HTTP

from datetime import datetime, date, timedelta

from models.crawler import Crawler

# import robocorp.workitems

import time
import random

class Browser:

    def __init__(self, site:str) -> None:

        # browser.goto(site)
        browser.configure(
            slowmo=10,
            browser_engine='chrome',
        )

        browser.goto(site)

        self.page = browser.page()

        try:
            self.page.click("button:text('Accept all')")
        except:
            print("No Cookies detected")
            pass

        print("Test Logging")
        self.search(1, 'Arts')

        print(self.page.url)

        self.crawler = Crawler()

        self.news = self.crawler.soup(self.page.url)
        print(self.news)

    # def search(self, phrase: str, section: str, month: int) -> None:
    def search(self, month:int, section: str) -> None:

        """Serch on New York Times for user's news"""

        self.page.click("data-testid=search-button")
        self.page.fill(".css-1u4s13l", "oi")
        self.page.click("button:text('Go')")

        time.sleep(3)

        # self.page.click("data-testid=search-date-dropdown-a")
        # self.page.click("button:text('Specific Dates')")

        self.filter_section(section)
        self.filter_time(month)
        self.order_news()
        # self.get_all_news()
            
    def filter_time(self, month: int) -> None:

        """Filter by month quantities"""

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

        if section not in ['Any', 'Arts', 'Books', 'Business', 'New York', 'Opinion', 'Sports', 'Travel', 'U.S.', 'World']:
            print("Invalid Section Error!")
            pass
        else:
            self.page.click("data-testid=search-multiselect-button")
            self.page.click(f"span:text('{section}')")
            self.page.click("data-testid=search-multiselect-button")

    def order_news(self):

        """Ordering by Newest"""
        
        self.page.select_option("data-testid=SearchForm-sortBy", "Sort by Newest")

    def get_all_news(self):
        
        """Click to get all news"""
        
        while True:
            try:
                self.page.click("button:text('Show More')")
            except:
                print("No More News on Page")
                break
