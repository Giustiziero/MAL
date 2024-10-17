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

    def write_anime_details(self, anime_name, anime_details):
        """
        Writes anime details into the 'anime_details_full' container.
        :param anime_id: Unique ID for the anime
        :param anime_name: Name of the anime (indexed for search)
        :param anime_details: Dictionary containing all anime details from the API
        """
        try:
            container = self.get_container('anime_details_full')

            id = str(anime_details['id'])
            del anime_details['id']
            # Document structure for the anime
            anime_document = {
                'id': id,
                'anime_name': anime_name,
                **anime_details  # Unpack the details dictionary into the document
            }

            # Insert the document into the container
            container.upsert_item(anime_document)
            print(f"Anime '{anime_name}' (ID: {id}) inserted/updated successfully.")
            return anime_document
        except Exception as e:
            raise Exception(f"Failed to insert anime details: {e}")
        