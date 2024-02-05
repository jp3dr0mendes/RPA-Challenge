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

    print("05/02")

    lib = WorkItems()
    workitem_input = lib.get_input_work_item().payload

    logging.info("Getting input data")

    if not isinstance(workitem_input["month"], int):
        logging.error("Invalid input workitem parameter")
        raise ValueError("""
                        The parameter "month" must be an integer.
                        {"news": str,"month": int, "section": str}""")
    
    elif not isinstance(workitem_input["news"], str):
        logging.error("Invalid input workitem parameter")
        raise ValueError("""
                        The parameter "news" must be an str.
                        {"news": str,"month": int, "section": str}""")
    
    elif not workitem_input["section"] in ['Any', 'Arts', 'Books', 'Business', 'New York', 'Opinion', 'Sports', 'Travel', 'U.S.', 'World']:
        logging.error("Invalid section parameter!")
        raise ValueError("Section must be: 'Any', 'Arts', 'Books', 'Business', 'New York', 'Opinion', 'Sports', 'Travel', 'U.S.' or 'World'")
    
    else:
        logging.info("Input data processing...")
    # print(workitem_input)
    # print(lib)
    news_data      = Browser(int(workitem_input["month"]),workitem_input["section"],workitem_input["news"])
    table          = output_data(news_data.news)
    payloads       = create_work_item_payloads(table)

    # with open('output.json','w') as output_file:
    #     json.dump(payloads, output_file, indent=2)

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
        # print("aqui passsou ksjdfhsdas")
        # workitem.create_output_work_item(variables, files="workitem.txt")

        # print("salvando")
        # print(f'passou{payload}')

        logging.info(f"downloading {payload['Image_Link']}...")

        try:
            http.download(url=payload["Image_Link"], overwrite=True)
        except:
            logging.warning(f"Fail to download image: {payload['Image_Link']}")
            # raise SystemError("Fail to download image. Check your connection")
        path                  = payload["Image_Link"].split('/')[-1]
        payload["Image_Link"] = path

        logging.info(f"load output {payload}")

        try:
            workitem.create_output_work_item(payload, files = path, save = True)
        except:
            logging.critical("Fail to load output item")
            raise SystemError("Failed on load output item. Try again!")
        
        logging.info("output item created")

    logging.info("all output items created")

    # print("salvandooooooooooooooooo522522885")
    # workitem.save_work_item()
    print(workitem)
    # print("sei la dog")

    wb = excel.create_workbook("workbook")

    wb.create_worksheet("news_data")
    wb.append_worksheet(name="news_data", content=data, header=True)
    wb.save("news_data.xlsx")

    print("gerando o excel")

    workitem.create_output_work_item(dict({"worksheet_output": "news_data.xlsx"}),files=["news_data.xlsx", "robot.log"], save = True)

def output_data(news_data: dict) -> bool:    
    return table.create_table(data=news_data)