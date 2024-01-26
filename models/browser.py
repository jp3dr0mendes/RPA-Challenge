from robocorp import browser
from robocorp.browser.keybord import Keybord
from robocorp.desktop import Desktop
# from robocorp.browser.cookies import Cookies

import robocorp.workitems


class Browser:
    def __init__(self) -> None:
        self.site:str = 'https://www.nytimes.com/'
        # self.site:str = 'https://www.google.com'
        
        try:
            browser.goto(self.site)
            page = browser.page()
            kb = Keybord(browser)
            dt = Desktop()
            
            page.fill("#searchTextField","test")
            kb.press_key(Keybord.KEY_ENTER)
            # page.click(".css-1bf34ii")
        except:
            print("Error on open browser")