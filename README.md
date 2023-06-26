# globant-challenge
This is my repo for globant challenge opportunity

## Objectives
Design a PoC for challenge #1 of Globant challenge 2023.
Implement PoC with Azure technologies and show the results.
## Requirements
Move historic data from files in CSV format to the new database.
Create a Rest API service to receive new data. This service must have:
    Each new transaction must fit the data dictionary rules.
    Be able to insert batch transactions (1 up to 1000 rows) with one request.
    Receive the data for each table in the same service.
    Keep in mind the data rules for each table.
Create a feature to backup for each table and save it in the file system in AVRO format.
Create a feature to restore a certain table with its backup.

## Arquitecture
![Alt text](challenge_arch.png)

## Proof of Functionality
### Load Files in ADLS Main
ADLS gen2 is deployed to store csv files.
RV: Raw Vault
UV: Universal Vault
DV: Dimensional Vault
![Alt text](image-1.png)

### ADLS Backup 
ADLS Gen 2 is deployed for backup files and tables' data. Uses pair region from main one.
Another aproach would be use the read-access geo-zone concept. It depends on the cost and complexity

### Azure Synapse for SQL database
Dedicated SQL Pool is deployed to query data.
Exist two type of tables: main for principals and backup for restore data

### Azure Data factory
Datafactory is used for move data from RV to UV or DV, depends on data's origin
Also is required for execute databricks notebooks
Exist two pipelines: one for ETL operations for main tables and the second for backup processes

### Azure Databricks
Databricks notebooks is required for transform data and load them into another path such as UV or DV

### Azure App Services for API solution
Solution uses app services to mount api.py script:

api.py executes flask solutions to implement API and connect to azure synapse using pyodbc to ingest registers

## Results

 - The firts pipeline extract, transform and load csv files into synapse main and backup tables
 - The second pipeline transform and load AVRO files into synapse main tables when it is required
 - Databricks enables data manipulation and analysis in the process
 - App services and flask implement the API solution.
