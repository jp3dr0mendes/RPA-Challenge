from robocorp.tasks import task
from robocorp import workitems
from RPA.Tables import Tables
from RPA.Excel.Files import Files
from models.browser import Browser

import json
import os

OUTPUT_DATA_PATH = '/output/output.json'

table = Tables()
excel = Files()
# def create_output(news_list: dict) -> list:



@task
def search_news():
    """Search a n"""
    inputs    = workitems.inputs

    input     = [i.payload for i in inputs]
    input     = input[0]
    print(inputs.released)
    news_data = Browser(int(input["month"]),input["section"],input["news"])
    
    # x = inputs.reserve()
    # del inputs
    
    table     = output_data(news_data.news)

    payloads = create_work_item_payloads(table)

    with open('output.json','w') as output_file:
        json.dump(payloads, output_file, indent=2)
    
    print("passou 1")

@task
def test_task():

    output_data = dict()    
    with open('output.json','r') as payload_file:
        output_data = json.load(payload_file)

    print(type(output_data))
    save_work_item_payloads(output_data)

    # os.mkdir('output_data')
    # os.chmod('output_data',os.W_OK)
    wb = excel.create_workbook("workbook")
    wb.create_worksheet("worksheet")
    wb.save("workbook.xlsx")

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

def save_work_item_payloads(data):
    for payload in data:
        # variables = dict(traffic_data=payload)
        workitems.outputs.create(payload)
        print(f'passou{payload}')

def output_data(news_data: dict) -> bool:    
    return table.create_table(data=news_data)

def create_excel_file(data: list):
    pass