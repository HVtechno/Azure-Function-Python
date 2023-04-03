# Azure Functions SQL Binding using Python

## Introduction
This repository is a sample for Azure Functions and SQL binding extension using Python. The type of bindings in this sample are:
- **Input Binding**: takes a SQL query and a parameter to run and returns the output to the function.
- **Output Binding**: takes a list of rows and inserts them into a table (this sample was tested with an Azure SQL Database)

For more details of the different types of bindings see the [Bindings Overview](https://github.com/Azure/azure-functions-sql-extension/blob/main/docs/BindingsOverview.md).

## Prerequisites
- The [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local#install-the-azure-functions-core-tools) version 4.x.
- Python versions that are [supported by Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/supported-languages#languages-by-runtime-version). For more information, see [How to install Python](https://wiki.python.org/moin/BeginnersGuide/Download)
- The [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) for Visual Studio Code, version 1.8.3 or a later version.
- An [Azure SQL](https://learn.microsoft.com/en-us/azure/azure-sql/?view=azuresql) database 

## Setup

### Install bundle
You can add the preview extension bundle by adding or replacing the following code in your host.json file:

```
{
  "version": "2.0",
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle.Preview",
    "version": "[4.*, 5.0.0)"
  }
}
```

### Update packages
Add this version of the library to your functions project with an update to the line for azure-functions== in the requirements.txt file in your Python Azure Functions project:
```
azure-functions==1.11.3b1
```

Following setting the library version, update your application settings to isolate the dependencies by adding PYTHON_ISOLATE_WORKER_DEPENDENCIES with the value 1 to your application settings. Locally, this is set in the local.settings.json file as seen below:
```
"PYTHON_ISOLATE_WORKER_DEPENDENCIES": "1"
```

### SQL connection string
Change the SQL connection string in the file local.settings.json
```
"SqlConnectionString": "Server={Azure SQL Server};Initial Catalog={Database name};Persist Security Info=False;User ID={user};Password={password};"
```
### Create table
In the database create a ToDo table:
```
CREATE TABLE [dbo].[dbo.Table_Invoice]
(
    Sales_Document VARCHAR(255),
    Date_Created DATE,
    Date_Download DATE,
    file_name varchar(255),
    invoice_amount varchar(255),
    invoice_number varchar(255),
    invoice_quantity varchar(255),
    PO_number varchar(255),
    Sales_Org varchar(255),
    Ship_To varchar(255),
    delivery varchar(255),
    material varchar(MAX),
    output varchar(255),
    shipment_number varchar(255),
    Dup_Value int,
    UniqueValue varchar(255) NOT NULL PRIMARY KEY
);
```
## Run the project

### HTTP trigger, write records to a SQL table
The function **Func_Invoice shows a SQL output binding** in a function.json file and a Python function that adds records to a table, using data provided in an HTTP POST request as a JSON body.

The following is binding data in the function.json file:
```
{
      "name": "InvoiceItems",
      "type": "sql",
      "direction": "out",
      "commandText": "dbo.Table_Invoice",
      "connectionStringSetting": "SqlConnectionString"
}
```

The script performs some additional actions based on the requirment from request input Json Body
- It calculates the current Date & Time
- Then, It create a Set of Unique ID's for the duplicated **[Sales_Document]**
- Later append the **[UniqueValue]** in the format of **[Sales_Document]+[ddmmhhss]+[Unique_Id]** with request Json Body into Dictionary
- Finally dump the Json body to SQL DB

Run the project and make a post request to the function Func_Invoice, you can use Postman or Azure Portal:
```
POST http://localhost:7071/api/Func_Invoice
content-type: application/json
Input body:

[
    {
      "Sales_Document": "65836538",
      "Date_Created" : "2023-04-04",
      "Date_Download": "2023-04-04",
      "file_name" : "INV_65836538.PDF",
      "invoice_amount" : "50.48",
      "invoice_number" : "7700817936",
      "invoice_quantity" : "2",
      "PO_number" : "TEST65836538",
      "Sales_Org" : "DE11",
      "Ship_To" : "29517803",
      "delivery" : "1028575146",
      "material" : "29881",
      "output" : "ZDE2"
    },
    {
      "Sales_Document": "65836538",
      "Date_Created" : "2023-04-04",
      "Date_Download": "2023-04-04",
      "file_name" : "INV_65836538_2.PDF",
      "invoice_amount" : "50.48",
      "invoice_number" : "7700817937",
      "invoice_quantity" : "2",
      "PO_number" : "TEST65836538_2",
      "Sales_Org" : "DE11",
      "Ship_To" : "29517803",
      "delivery" : "1028575146",
      "Material" : "29882",
      "output" : "ZDE2"
    }
]

Output Body:

[
  {
    "Sales_Document": "65836538",
    "Date_Created": "2023-04-04",
    "Date_Download": "2023-04-04",
    "file_name": "INV_65836538.PDF",
    "invoice_amount": "50.48",
    "invoice_number": "7700817936",
    "invoice_quantity": "2",
    "PO_number": "TEST65836538",
    "Sales_Org": "DE11",
    "Ship_To": "29517803",
    "delivery": "1028575146",
    "material": "29881",
    "output": "ZDE2",
    "Dup_Value": 1,
    "UniqueValue": "65836538-0304222002-1"
  },
  {
    "Sales_Document": "65836538",
    "Date_Created": "2023-04-04",
    "Date_Download": "2023-04-04",
    "file_name": "INV_65836538_2.PDF",
    "invoice_amount": "50.48",
    "invoice_number": "7700817937",
    "invoice_quantity": "2",
    "PO_number": "TEST65836538_2",
    "Sales_Org": "DE11",
    "Ship_To": "29517803",
    "delivery": "1028575146",
    "material": "29882",
    "output": "ZDE2",
    "Dup_Value": 2,
    "UniqueValue": "65836538-0304222002-2"
  }
]
```
