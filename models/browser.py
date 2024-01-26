from robocorp import browser
from datetime import datetime, date, timedelta
# import robocorp.workitems

import time
import random

class Browser():

    def __init__(self, site:str) -> None:

        browser.goto(site)
        browser.configure(
            slowmo=100,
        )

        self.page = browser.page()

        try:
            self.page.click("button:text('Accept all')")
        except:
            pass
        
        self.search(1)

    # def search(self, phrase: str, section: str, month: int) -> None:
    def search(self, month:int) -> None:

        """Serch on New York Times for user's news"""

        self.page.click("data-testid=search-button")
        self.page.fill(".css-1u4s13l", "oi")
        self.page.click("button:text('Accept all')")
        self.page.click("button:text('Go')")
        self.page.click("data-testid=search-date-dropdown-a")

        self.filter_time(month)

    def filter_time(self, month: int) -> None:

        if month == 0 or month == 1:
            date_user = datetime.now()
        else:
            date_user = datetime.now() - timedelta(days=30*month)

        self.page.fill("#startDate", "{date_user.month}/01/{date_user.year}")


        if date_user.month == 2:

            if datetime.now().year // 4 != 0:
                self.page.fill("#endDate", "28/{date_user.month}/28/2024")
            else:
                self.page.fill("#endDate", "29/{date_user.month}/29/2024")

        elif date_user.month in [1,3,5,7,8,10,12]:
            self.page.fill("#endDate", "{date_user.month}/31/2024")
        else:
            self.page.fill("#endDate", "{date_user.month}/30/2024")

# class Crawler:

#     """Content Analyst"""
    
#     def __init__(self):
#         pass