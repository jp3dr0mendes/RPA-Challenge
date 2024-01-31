from robocorp.tasks import task
from robocorp import workitems
# from robocorp.robot.api
from RPA.Tables import Tables
from RPA.Excel.Files import Files
from RPA.PDF import PDF
from models.browser import Browser

import json
import os

table = Tables()
excel = Files()

@task
def test_task():

    output_data = dict()    
    with open('output.json','r') as payload_file:
        output_data = json.load(payload_file)

    print(type(output_data))
    print("vamo ve se agr vai neh")
    # save_work_item_payloads(output_data)

    output = workitems.outputs

    # for payload in output_data:
    #     output.create(payload)

    # os.mkdir('output_data')
    # os.chmod('output_data',os.W_OK)
    wb = excel.create_workbook("workbook")
    wb.create_worksheet("worksheet")
    wb.save("workbooksdffsdfds.xlsx")

    pdf = PDF()
    pdf.active_pdf_document

def save_work_item_payloads(data):
    for payload in data:
        # variables = dict(traffic_data=payload)
        print("aqui passsou ksjdfhsdas")
        workitems.outputs.create(payload)
        print(f'passou{payload}')