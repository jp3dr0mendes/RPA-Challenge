from robocorp import browser
import robocorp.workitems

class Browser:
    def __init__(self, path: str) -> None:
        
        inputs  = robocorp.workitems.Inputs()
        item    = inputs.reserve()  
        payload = item.payload

        self.site:str = 'https://www.nytimes.com/'
        
        try:
            browser.goto(self.site)
        except:
            print("Error on open browser")