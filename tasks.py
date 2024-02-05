from robocorp.tasks import task

from RPA.Tables import Tables
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
from RPA.Robocorp.WorkItems import WorkItems

from models.browser import Browser

import json
import logging

table = Tables()
excel = Files()
http = HTTP()

logging.basicConfig(level=logging.INFO,
                    filename="robot.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")

@task
def search_news():

    """Search a news and Extract the information"""

    lib = WorkItems()
    w = lib.get_input_work_item().payload
    print(w)
    print(lib)
    news_data = Browser(int(w["month"]),w["section"],w["news"])

    table     = output_data(news_data.news)

    payloads = create_work_item_payloads(table)

    with open('output.json','w') as output_file:
        json.dump(payloads, output_file, indent=2)

    lib.save_work_item()

    save_work_item_payloads(payloads, lib)
    
    print("passou 1")

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

def save_work_item_payloads(data, workitem):

    for payload in data:
        variables = dict(traffic_data=payload)
        print("aqui passsou ksjdfhsdas")
        # workitem.create_output_work_item(variables, files="workitem.txt")

        # print("salvando")
        print(f'passou{payload}')

        http.download(url=payload["Image_Link"], overwrite=True)

        path                  = payload["Image_Link"].split('/')[-1]
        payload["Image_Link"] = path

        workitem.create_output_work_item(payload, files = path, save = True)

    # print("salvandooooooooooooooooo522522885")
    # workitem.save_work_item()
    print(workitem)
    # print("sei la dog")

    wb = excel.create_workbook("workbook")
    wb.create_worksheet("worksheet")
    wb.append_worksheet(name="news_data", content=data, header=True)
    wb.save("news_data.xlsx")
    workitem.create_output_work_items(files="news_data.xlsx")

def output_data(news_data: dict) -> bool:    
    return table.create_table(data=news_data)