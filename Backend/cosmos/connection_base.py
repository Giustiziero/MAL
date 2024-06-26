from azure.cosmos import CosmosClient, exceptions
from azure.cosmos.partition_key import PartitionKey
import pandas as pd
# Get connection info
from dotenv import load_dotenv
import os
import pdb
# Azure Cosmos DB connection details
load_dotenv()
HOST = os.getenv('ACCOUNT_HOST')
MASTER_KEY = os.getenv('ACCOUNT_KEY')
USER_AGENT = 'MALREC/1.0'
DATABASE_ID = 'MalRecCosmos'
CONTAINER_ID = 'cos_sim_scores'

def process_mat(container):
    df = pd.read_csv('/Users/giulianotissot/Desktop/Cs_folders/MAL/MAL/Temp_data/cosine_sim_mat.csv', index_col=0)
    for index, row in enumerate(df.iterrows()):
        row_index_name = row[0]
        pd_series = row[1]
        item = {
            'id': str(index),  # unique id for the document
            'anime_name': row_index_name,
            'scores_array': list(pd_series.values)
        }
        print(f"Item {index} created")
        try:
            container.create_item(body=item)
        except:
            continue

def create_database():
    # Initialize the Cosmos client
    client = CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent=USER_AGENT)
    try:
        # setup database for this sample
        try:
            db = client.create_database(id=DATABASE_ID)
            print('Database with id \'{0}\' created'.format(DATABASE_ID))

        except exceptions.CosmosResourceExistsError:
            db = client.get_database_client(DATABASE_ID)
            print('Database with id \'{0}\' was found'.format(DATABASE_ID))

         # setup container for this app
        try:
            container = db.create_container(id=CONTAINER_ID, partition_key=PartitionKey(path='/anime_name'))
            print('Container with id \'{0}\' created'.format(CONTAINER_ID))

        except exceptions.CosmosResourceExistsError:
            container = db.get_container_client(CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(CONTAINER_ID))

        process_mat(container)

    except exceptions.CosmosHttpResponseError as e:
        print('\ncreate_database has caught an error. {0}'.format(e.message))

    finally:
            print("\ncreate_database done")

# create_database()

def upload_indexing_table():
    df = pd.read_csv('/Users/giulianotissot/Desktop/Cs_folders/MAL/MAL/Temp_data/cosine_sim_mat.csv', index_col=0)
    container_id = 'anime_details'
    client = CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent=USER_AGENT)
    db = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(container_id)
    index_dict = {anime_name: index for index, anime_name in enumerate(list(df.columns))}
    item = {
        'id': 'anime_indexes',
        'type': 'ByAnimeName',
        'index_dict': index_dict
    } 
    container.upsert_item(body=item)
    # container.upsert_item(body=item)

upload_indexing_table()