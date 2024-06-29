import pandas as pd
from azure.cosmos import CosmosClient, exceptions
from azure.cosmos.partition_key import PartitionKey
from dotenv import load_dotenv
import os
import pdb
import time
# Azure Cosmos DB connection details


def get_index_dict():
    load_dotenv()
    HOST = os.getenv('ACCOUNT_HOST')
    MASTER_KEY = os.getenv('ACCOUNT_KEY')
    USER_AGENT = 'MALREC/1.0'
    DATABASE_ID = 'MalRecCosmos'
    CONTAINER_ID = 'anime_details'

    client = CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent=USER_AGENT)

    try:
        try:
            db = client.get_database_client(DATABASE_ID)
            print('Database with id \'{0}\' was found'.format(DATABASE_ID))
        except:
            print('Error: Database with id \'{0}\' not found'.format(DATABASE_ID))
            pass
        # setup container for this sample
        try:
            container = db.get_container_client(CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(CONTAINER_ID))
        except:
            print('Container with id \'{0}\' was not found'.format(CONTAINER_ID))
            pass

        try: 
            start = time.time()

            response = container.read_item(item='anime_indexes',partition_key='ByAnimeName')
            index_dict = response.get('index_dict')
            print(len(response.get('index_dict')))
            dur = time.time() - start
            print(f"query took {dur}")
            return index_dict
        except Exception as e :
            print(f"second query failure \n {e}")

    except exceptions.CosmosHttpResponseError as e:
        print('\get_index_dict has caught an error. {0}'.format(e.message))

    finally:
            print("\get_index_dict done")

def get_similar_animes(anime_name, index_dict, top_n=25):
    load_dotenv()
    HOST = os.getenv('ACCOUNT_HOST')
    MASTER_KEY = os.getenv('ACCOUNT_KEY')
    USER_AGENT = 'MALREC/1.0'
    DATABASE_ID = 'MalRecCosmos'
    CONTAINER_ID = 'cos_sim_scores'

    client = CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent=USER_AGENT)
    # setup database for this sample
    try:
        try:
            db = client.get_database_client(DATABASE_ID)
            print('Database with id \'{0}\' was found'.format(DATABASE_ID))
        except:
            print('Error: Database with id \'{0}\' not found'.format(DATABASE_ID))
            pass
        # setup container for this sample
        try:
            container = db.get_container_client(CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(CONTAINER_ID))
        except:
            print('Container with id \'{0}\' was not found'.format(CONTAINER_ID))
            pass
        
        ### Querying method
        # try: 
        #     start =time.time()
        #     query = "SELECT * FROM c WHERE c.anime_name=@anime_name"
        #     parameters = [
        #         {"name": "@anime_name", "value": anime_name}
        #     ]
        #     items = list(container.query_items(
        #         query=query,
        #         parameters=parameters,
        #         enable_cross_partition_query=True
        #     ))
        #     dur = time.time() - start
        #     print(len(items))
        #     print(f"query took {dur}")
        # except e: 
        #     print(f"query had some issue: \n {e}")

        ### Secondary method for getting the index_dict -- too slow
        # try: 
        #     start = time.time()

        #     query = "SELECT c.anime_name FROM c ORDER BY c.id ASC"
        #     items = list(container.query_items(
        #         query=query,
        #         enable_cross_partition_query=True
        #     ))
            
            

        #     dur = time.time() - start
        #     print(f"query took {dur}")
        # except:
        #     print(f"second query failure \n {e.message}")

        ### Querying direct through this method is faster
        start = time.time()
        anime_id = index_dict[anime_name]
        response = container.read_item(item=str(anime_id), partition_key=anime_name)
        scores_arr = response.get('scores_array')
        print(len(scores_arr))
        dur = time.time() - start
        print(f"query direct took {dur}")

        sim_scores = process_sim_scores(scores_arr, index_dict, top_n)
        return sim_scores
    except exceptions.CosmosHttpResponseError as e:
        print('\nget_similar_anime has caught an error. {0}'.format(e.message))

    finally:
            print("\get_similar_anime done")

    # similar_animes = similarity_df[anime_name].sort_values(ascending=False)
    # similar_animes = similar_animes.head(top_n + 1).iloc[1:]  # Exclude the anime itself
    # similar_animes = (similar_animes * 100).round(1)
    # return similar_animes

def process_sim_scores(scores_arr, index_dict, top_n):
    # Create a list of anime names based on the indexes
    index_to_anime = {v: k for k, v in index_dict.items()}
    anime_names = [index_to_anime[i] for i in range(len(scores_arr))]

    # Create the pandas series
    anime_scores = pd.Series(data=scores_arr, index=anime_names)

    index_dict = scores_arr

    similar_animes = anime_scores.sort_values(ascending=False)
    similar_animes = similar_animes.head(top_n + 1).iloc[1:]  # Exclude the anime itself
    similar_animes = (similar_animes * 100).round(1)
    print(similar_animes)
    return similar_animes

index_dict = get_index_dict()
get_similar_animes("Naruto", index_dict)
