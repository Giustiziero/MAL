import pandas as pd
from azure.cosmos import CosmosClient, exceptions
from azure.cosmos.partition_key import PartitionKey
from dotenv import load_dotenv
import os
import time

# Define custom exceptions for specific error conditions
class DatabaseNotFoundError(Exception):
    pass

class ContainerNotFoundError(Exception):
    pass

class ItemNotFoundError(Exception):
    pass

class DatabaseHandler:
    def __init__(self, database_id):
        load_dotenv()
        self.host = os.getenv('ACCOUNT_HOST')
        self.master_key = os.getenv('ACCOUNT_KEY')
        self.user_agent = 'MALREC/1.0'
        self.client = CosmosClient(self.host, {'masterKey': self.master_key}, user_agent=self.user_agent)
        self.db_id = self.client.get_database_client(database_id)
        self.db = self.get_database()

    def get_database(self):
        try:
            db = self.client.get_database_client(self.db_id)
            print(f"Database '{self.db_id}' found.")
            return db
        except Exception as e:
            raise DatabaseNotFoundError(f"Database '{self.db_id}' not found: {str(e)}")

    def get_container(self, container_id):
        try:
            container = self.db.get_container_client(container_id)
            print(f"Container '{container_id}' found.")
            return container
        except Exception as e:
            raise ContainerNotFoundError(f"Container '{container_id}' not found: {str(e)}")

    def read_item(self, container, item_id, partition_key):
        try:
            response = container.read_item(item=item_id, partition_key=partition_key)
            return response
        except exceptions.CosmosHttpResponseError as e:
            raise ItemNotFoundError(f"Item with ID '{item_id}' and partition key '{partition_key}' not found: {e.message}")

    def create_container_if_not_exists(self, container_id, partition_key):
        """
        Checks if the container exists, and creates it if it doesn't.
        :param container_id: ID of the container to create.
        :param partition_key: Partition key for the container (e.g., "/anime_name").
        """
        try:
            # Try to get the container, create it if it does not exist
            container = self.db.create_container_if_not_exists(
                id=container_id,
                partition_key=PartitionKey(path=partition_key)
            )
            print(f"Container '{container_id}' is ready.")
            return container
        except exceptions.CosmosHttpResponseError as e:
            raise Exception(f"Failed to create or access container: {e.message}")

    def write_anime_details(self, anime_id, anime_name, anime_details):
        """
        Writes anime details into the 'anime_details_full' container.
        :param anime_id: Unique ID for the anime
        :param anime_name: Name of the anime (indexed for search)
        :param anime_details: Dictionary containing all anime details from the API
        """
        try:
            container = self.get_container('anime_details_full')

            # Document structure for the anime
            anime_document = {
                'id': anime_id,
                'anime_name': anime_name,
                **anime_details  # Unpack the details dictionary into the document
            }

            # Insert the document into the container
            container.upsert_item(anime_document)
            print(f"Anime '{anime_name}' (ID: {anime_id}) inserted/updated successfully.")
        except Exception as e:
            raise Exception(f"Failed to insert anime details: {e}")
        
class AnimeService:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def get_index_dict(self):
        try:
            container = self.db_handler.get_container('anime_details')
            start = time.time()
            response = self.db_handler.read_item(container, 'anime_indexes', 'ByAnimeName')
            index_dict = response.get('index_dict')
            print(f"Index dictionary length: {len(index_dict)}")
            print(f"Query took {time.time() - start:.2f} seconds")
            return index_dict
        except (DatabaseNotFoundError, ContainerNotFoundError, ItemNotFoundError) as e:
            print(f"Error retrieving index dictionary: {e}")
            return None

    def get_similar_animes(self, anime_name, index_dict, top_n=25):
        try:
            container = self.db_handler.get_container('cos_sim_scores')
            anime_id = index_dict[anime_name]
            start = time.time()
            response = self.db_handler.read_item(container, str(anime_id), anime_name)
            scores_arr = response.get('scores_array')
            print(f"Query took {time.time() - start:.2f} seconds")
            return self.process_sim_scores(scores_arr, index_dict, top_n)
        except KeyError:
            raise ValueError(f"Anime '{anime_name}' not found in index.")
        except (DatabaseNotFoundError, ContainerNotFoundError, ItemNotFoundError) as e:
            print(f"Error retrieving similar animes: {e}")
            return None

    def process_sim_scores(self, scores_arr, index_dict, top_n):
        index_to_anime = {v: k for k, v in index_dict.items()}
        anime_names = [index_to_anime[i] for i in range(len(scores_arr))]
        anime_scores = pd.Series(data=scores_arr, index=anime_names)
        similar_animes = anime_scores.sort_values(ascending=False)
        similar_animes = similar_animes.head(top_n + 1).iloc[1:]  # Exclude the anime itself
        similar_animes = (similar_animes * 100).round(1)
        print(similar_animes)
        return similar_animes
    
if __name__ == '__main__':
    db_handler = DatabaseHandler('MalRecCosmos')
    anime_service = AnimeService(db_handler)

    index_dict = anime_service.get_index_dict()
    print(list(index_dict.items())[:10])
    if index_dict:
        try:
            anime_service.get_similar_animes("Naruto", index_dict)
        except ValueError as e:
            print(f"Error: {e}")

    # New stuff
    # Create Container
    partition_key = '/anime_name'
    container_id = 'anime_details_full'
    db_handler.create_container_if_not_exists(container_id, partition_key)

    # # Test container
    from Utils.MAL_connection.MAL_API_Fetcher import MAL_API_Fetcher
    fetcher = MAL_API_Fetcher()
    anime_name = 'Naruto'
    anime_details = fetcher.get_anime_details_from_name(anime_name)
    print((anime_details['id'], anime_details['title']))

    id = anime_details['id']
    del anime_details['id']
    # anime_details_test = {
    #     'description': 'A story about ninjas...',
    #     'genre': ['Action', 'Adventure']
    # }

    db_handler.write_anime_details(str(id), anime_name, anime_details)
    print("succesfully upserted my item")
    container = db_handler.get_container(container_id)
    print(db_handler.read_item(container, '20', 'Naruto'))
