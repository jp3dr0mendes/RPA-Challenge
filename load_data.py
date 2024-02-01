from robocorp.tasks import task
# from robocorp import workitems
# from robocorp.robot.api
from RPA.Tables import Tables
from RPA.Robocorp.WorkItems import State, WorkItems
from RPA.Excel.Files import Files
from RPA.PDF import PDF
from models.browser import Browser

import json
import os

table = Tables()
excel = Files()

@task
def test_task():

    # output_data = dict()    
    # with open('output.json','r') as payload_file:
    #     output_data = json.load(payload_file)

    output_data = []

    workitems = WorkItems()

    for item in workitems.outputs:
        print(item)
        output_data.append(item.payload)

    # output_data = dict(output_data)

    print(output_data)

    print(type(output_data))
    print("vamo ve se agr vai neh")
    # save_work_item_payloads(output_data)

    # workitems = WorkItems()

    # for payload in output_data:
    #     output.create(payload)

    # os.mkdir('output_data')
    # os.chmod('output_data',os.W_OK)
    wb = excel.create_workbook("workbook")
    wb.create_worksheet("worksheet")
    wb.append_worksheet(name="worksheet", content=output_data, header=True)
    # for item in output_data:
    #     wb.insert_rows(item)
    wb.save("workbooksdffsdfds.xlsx")
    workitems.get_input_work_item()
    workitems.create_output_work_item(dict(),files="workbooksdffsdfds.xlsx")




def save_work_item_payloads(data):
    for payload in data:
        # variables = dict(traffic_data=payload)
        print("aqui passsou ksjdfhsdas")
        workitems.outputs.create(payload)
        print(f'passou{payload}')