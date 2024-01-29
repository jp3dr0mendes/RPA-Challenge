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

    payload = create_work_item_payloads(table)
    save_work_item_payloads(payload)
    
    # payload = []

    # for row in table:
    #     item = dict(
    #         Title       = row['Title'],
    #         Description = row['Description'],
    #         Date        = row['Date'],
    #         Any_Money   = row['Any Money'],
    #         Image_Link  = row['Image Link'],
    #     )
    #     payload.append(item)

    # output = dict(traffic_data=payload)
    # workitems.outputs.create()
    # workitems.outputs.create(output)


    


# @task
# def filter_news():

# @task
# def get_news_data():

# @task

def create_work_item_payloads(traffic_data):
    payloads = []
    for row in traffic_data:
        payload = dict(
            Title=row["Title"],
            Description=row["Description"],
            Date=row["Date"],
            Any_Money=row["Any Money"],
            Image_Link=row["Image Link"],
        )
        payloads.append(payload)
    return payloads

def save_work_item_payloads(payloads):
    for payload in payloads:
        variables = dict(traffic_data=payload)
        workitems.outputs.create(variables)

def output_data(news_data: dict) -> bool:
    # column = [t.key for t in news_data if t not in column]
    
    return table.create_table(data=news_data)

============================================================================

from robocorp import workitems
from robocorp.tasks import task
from RPA.HTTP import HTTP
from RPA.JSON import JSON
from RPA.Tables import Tables

http = HTTP()
json = JSON()
table = Tables()

TRAFFIC_JSON_FILE_PATH = "output/traffic.json"

# JSON data keys
COUNTRY_KEY = "SpatialDim"
YEAR_KEY = "TimeDim"
RATE_KEY = "NumericValue"
GENDER_KEY = "Dim1"

@task
def produce_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System automation.
    Produces traffic data work items.
    """
    http.download(
        url="https://github.com/robocorp/inhuman-insurance-inc/raw/main/RS_198.json",
        target_file=TRAFFIC_JSON_FILE_PATH,
        overwrite=True,
    )
    traffic_data = load_traffic_data_as_table()
    filtered_data = filter_and_sort_traffic_data(traffic_data)
    filtered_data = get_latest_data_by_country(filtered_data)
    payloads = create_work_item_payloads(filtered_data)
    save_work_item_payloads(payloads)

@task
def consume_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System automation.
    Consumes traffic data work items.
    """
    print("consume")

def load_traffic_data_as_table():
    json_data = json.load_json_from_file(TRAFFIC_JSON_FILE_PATH)
    return table.create_table(json_data["value"])

def filter_and_sort_traffic_data(data):
    max_rate = 5.0
    both_genders = "BTSX"
    table.filter_table_by_column(data, RATE_KEY, "<", max_rate)
    table.filter_table_by_column(data, GENDER_KEY, "==", both_genders)
    table.sort_table_by_column(data, YEAR_KEY, False)
    return data

def get_latest_data_by_country(data):
    data = table.group_table_by_column(data, COUNTRY_KEY)
    latest_data_by_country = []
    for group in data:
        first_row = table.pop_table_row(group)
        latest_data_by_country.append(first_row)
    return latest_data_by_country

def create_work_item_payloads(traffic_data):
    payloads = []
    for row in traffic_data:
        payload = dict(
            country=row[COUNTRY_KEY],
            year=row[YEAR_KEY],
            rate=row[RATE_KEY],
        )
        payloads.append(payload)
    return payloads

def save_work_item_payloads(payloads):
    for payload in payloads:
        variables = dict(traffic_data=payload)
        workitems.outputs.create(variables)