from robocorp.tasks import task
from robocorp import workitems

from models.browser import Browser

OUTPUT_FILE_PATH = "/output"

# def create_output(news_list: dict) -> list:



@task
def search_news():
    """Search a n"""
    inputs = workitems.inputs
    input  = [i.payload for i in inputs]
    input  = input[0]
    # for t in test:
    #     print(t.payload)
    news_data = Browser(input["months"],input["section"],input["news"])
    print(news_data)


# @task
# def filter_news():

# @task
# def get_news_data():

# @task
# def output_data()
