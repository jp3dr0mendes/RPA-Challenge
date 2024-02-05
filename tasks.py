from robocorp.tasks import task
from robocorp import workitems
from RPA.Tables import Tables
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
from models.browser import Browser
from RPA.Robocorp.WorkItems import State, WorkItems
import json
import os

table = Tables()
excel = Files()
http = HTTP()
# def create_output(news_list: dict) -> list:



@task
def search_news():
    """Search a n"""
    # inputsw    = workitems

    # inputs     = [i.payload for i in inputsw.inputs]
    # input     = inputs[0]
    # print(inputs.released)

    lib = WorkItems()
    w = lib.get_input_work_item().payload
    print(w)
    print(lib)
    news_data = Browser(int(w["month"]),w["section"],w["news"])
    
    # x = inputs.reserve()
    # del inputs
    
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

def save_work_item_payloads(data, teste):
    with open('teste.txt','w') as file:
        file.write("testando isso aqui")

    for payload in data:
        variables = dict(traffic_data=payload)
        print("aqui passsou ksjdfhsdas")
        # teste.create_output_work_item(variables, files="teste.txt")

        print("salvando")
        print(f'passou{payload}')

        http.download(url=payload["Image_Link"], overwrite=True)

        path                  = payload["Image_Link"].split('/')[-1]
        payload["Image_Link"] = path

        teste.create_output_work_item(payload, files = path, save = True)

    print("salvandooooooooooooooooo522522885")
    # teste.save_work_item()
    print(teste)
    print("sei la dog")

def output_data(news_data: dict) -> bool:    
    return table.create_table(data=news_data)

def create_excel_file(data: list):
    pass