from robocorp.tasks import task

from models.browser import Browser

@task
def search_news():
    """Search a n"""
    Browser('https://www.nytimes.com/')
    # open_website()
    """Extração de dados de um site de notícias"""
    # message = "Hello"
    # message = message + " World!"

# def open_website():
#     browser.goto("https://google.com")