from flask import Flask, request
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import pyodbc
import logging
import datetime

sysdatetime = datetime.datetime.now()
# Logging configs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log files path
log_file_path = f'globant-challenge/api/logs/log_apiload_{sysdatetime}.log'

# Initialazing logger
logger = logging.getLogger(__name__)

# Config initializer
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)

#Add handler to logger
logger.addHandler(file_handler)

logger.info('Inittializing App')
app = Flask(__name__)

datatype_rules = {
    'jobs': ['int', 'string'],
    'hired_employees': ['int', 'string','datetime','int','int'],
    'departments': ['int', 'string']
}

logger.info('Azure Synapse Analytics SQL pool connection details')
server = 'globant-challenge-workspace.sql.azuresynapse.net'
database = 'gcdedsqlpool'
driver = '{ODBC Driver 17 for SQL Server}'

logger.info('Azure AD and Key Vault configuration')
key_vault_url = 'https://gchallenge-vault.vault.azure.net'
secret_names = ['client_id', 'client_secret', 'tenant_id']

credential = DefaultAzureCredential()

logger.info('Getting secrets')
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
secrets = {secret_name: secret_client.get_secret(secret_name).value for secret_name in secret_names}

# Endpoint for receiving new data with authentication and authorization
@app.route('/api/insert', methods=['POST'])
def insert_data():
    logger.info('Getting input json')
    data = request.json

    # Validate data against data dictionary rules
    table_name = data.get('table')
    fields = data.get('data')

    if table_name not in datatype_rules.keys():
        logger.error('error: Invalid table name')

    if not all(type(field) in fields for field in datatype_rules[table_name]):
        logger.error('error: Data does not fit data dictionary rules')

    try:
        logger.info('Establish connection to Azure Synapse Analytics SQL pool')
        conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};Authentication=ActiveDirectoryInteractive"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        logger.info(f'inserting {len(list(fields))} registers in {table_name}')
        if table_name == 'hired_employees':
            
            query = f"""INSERT INTO {table_name} 'employmee_id', 'employee','date_time','department_id','job_id' 
                        VALUES ({fields[0]}, {fields[1]}, {fields[2]},{fields[3]},{fields[4]})"""
            cursor.executemany(query, fields)
        elif table_name == 'jobs':
            query = f"""INSERT INTO {table_name} 'job_id', 'job' 
                        VALUES ({fields[0]}, {fields[1]})"""
            cursor.executemany(query, fields)
        elif table_name == 'departments':
            query = f"""INSERT INTO {table_name} 'department_id', 'department' 
                        VALUES ({fields[0]}, {fields[1]})"""
            cursor.executemany(query, fields)
        conn.commit()

        logger.error('Data inserted succesfully')

    except Exception as e:
        error = str(e)
        logger.error('Error while connecting with azure {error)}')

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run()
