from robocorp import browser
import robocorp.workitems

class Browser:
    def __init__(self, path: str) -> None:
        # self.site:str = 'https://www.nytimes.com/'
        self.site:str = 'https://www.google.com'
        
        try:
            browser.goto(self.site)
        except:
            print("Error on open browser")