import logging
import json
import azure.functions as func
from datetime import datetime

def main(req: func.HttpRequest, InvoiceItems: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request and ready to insert data in SQL DB')
    
    req_body = req.get_json()
    
    # Get current date and time
    Current_now = datetime.now()
    Current_Time = Current_now.strftime("%d%m%H%M%S")
    # Create a set of unique IDs to check for duplicates
    unique_ids = set()
    counter = 1 
    for items in req_body: 
        if items['Sales_Document'] in unique_ids:
            # If the Sales_document is a duplicated, assign 1st sales_doc json body with 1 & next with increment value
            items['Dup_Value'] = counter + 1
            counter += 1
            items['UniqueValue'] = str(items['Sales_Document']) + "-" + Current_Time + "-" + str(items['Dup_Value'])
        else:
            # If the sales_document is unique, assign a value of 1 and add to the set of unique IDs
            items["Dup_Value"] = 1
            unique_ids.add(items["Sales_Document"])
            items['UniqueValue'] = str(items['Sales_Document']) + "-" + Current_Time + "-" + str(items['Dup_Value'])

    sql_rows = func.SqlRowList(map(lambda r: func.SqlRow.from_dict(r), req_body))
    InvoiceItems.set(sql_rows)
        
    logging.info(json.dumps(req_body))
    return func.HttpResponse(
            body=json.dumps(req_body),
            status_code=201,
            mimetype="application/json"
        )