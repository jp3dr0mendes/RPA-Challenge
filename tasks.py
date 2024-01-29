from robocorp.tasks import task
from robocorp import workitems
from RPA.Tables import Tables
from RPA.Excel.Files import Files
# from robocorp.log 

from models.browser import Browser

OUTPUT_FILE_PATH = "/output"

table = Tables()
excel = Files()
# def create_output(news_list: dict) -> list:



@task
def search_news():
    """Search a n"""
    inputs    = workitems.inputs
    input     = [i.payload for i in inputs]
    input     = input[0]
    news_data = Browser(int(input["month"]),input["section"],input["news"])
    table     = output_data(news_data.news)

    payload = []

    for row in table:
        item = dict(
            Title       = row['Title'],
            Description = row['Description'],
            Date        = row['Date'],
            Any_Money   = row['Any Money'],
            Image_Link  = row['Image Link'],
        )
        payload.append(item)

    output = dict(traffic_data=payload)
    workitems.outputs.create()
    workitems.outputs.create(output)

    


# @task
# def filter_news():

# @task
# def get_news_data():

# @task
def output_data(news_data: dict) -> bool:
    # column = [t.key for t in news_data if t not in column]
    
    return table.create_table(data=news_data)
