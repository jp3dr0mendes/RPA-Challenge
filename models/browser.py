from robocorp import browser

from RPA.HTTP import HTTP

from datetime import datetime, date, timedelta

from models.crawler import Crawler

# import robocorp.workitems

import time
import random

class Browser:

    def __init__(self, months_qtd: int, section: str, news_user: str) -> None:

        # browser.goto(site)
        browser.configure(
            slowmo=10,
            browser_engine='chrome',
        )

        self.site = 'https://www.nytimes.com/'
        self.page    = browser.page()
        self.crawler = Crawler()

        browser.goto(self.site)

        print(f"""
                ----------------------------------------------------------------
                               Acessing: {self.page.url}
                ----------------------------------------------------------------
                """)
        
        time.sleep(random.randint(1,5))
        
        try:
            self.page.click("button:text('Accept all')")
        except:
            print("No Cookies detected")
            pass

        print("""
                ----------------------------------------------------------------
                                  Cookies Accepted
                ----------------------------------------------------------------
                """)


        self.search(news_user, months_qtd, section)

        print("""
                ----------------------------------------------------------------
                                   Ordering by Newest
                ----------------------------------------------------------------
                """)

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

        print(self.news)

    # def search(self, phrase: str, section: str, month: int) -> None:
    def search(self, news: str, month:int, section: str) -> None:

        """Serch on New York Times for user's news"""

        print(f"""
                ----------------------------------------------------------------
                                 Searching for {news}
                ----------------------------------------------------------------
                """)
        time.sleep(random.randint(1,5))
        self.page.click("data-testid=search-button")
        time.sleep(random.randint(1,5))
        self.page.fill(".css-1u4s13l", "oi")
        time.sleep(random.randint(1,5))
        self.page.click("button:text('Go')")

        # time.sleep(3)

        print(f"""
                ----------------------------------------------------------------
                          Filter by  |  Section  | Months  |
                        -------------+-----------+---------+
                                     | {section} | {month} |
                        -------------+-----------+---------=
                ----------------------------------------------------------------
                """)

        self.filter_section(section)
        self.filter_time(month)
            
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

