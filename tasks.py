from robocorp.tasks import task
from robocorp import browser
from models.browser import Browser

@task
def robot_test():
    Browser()
    # open_website()
    """Extração de dados de um site de notícias"""
    # message = "Hello"
    # message = message + " World!"

# def open_website():
#     browser.goto("https://google.com")