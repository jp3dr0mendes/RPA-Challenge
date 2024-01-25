from robocorp import browser
import robocorp.workitems

class Browser:
    def __init__(self) -> None:
        self.site:str = 'https://www.nytimes.com/'
        # self.site:str = 'https://www.google.com'
        
        try:
            browser.goto(self.site)
            page = browser.page()
            
            page.fill("#searchTextField","test")
            page.click(".css-1bf34ii")
        except:
            print("Error on open browser")