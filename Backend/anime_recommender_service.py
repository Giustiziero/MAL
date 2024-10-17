import pandas as pd
from azure.cosmos import CosmosClient, exceptions
from azure.cosmos.partition_key import PartitionKey
from dotenv import load_dotenv
import os
import time
from database_handler import DatabaseHandler, DatabaseNotFoundError, ContainerNotFoundError, ItemNotFoundError

class AnimeRecommenderService:
    def __init__(self, db_handler, mal_fetcher):
        self.db_handler = db_handler
        self.mal_fetcher = mal_fetcher

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

    def get_anime_details(self, anime_name):
        """
        Checks if we already have anime_details in the db, and fetches from an external source if not.
        :param anime_name: Name of the anime to look up
        :return: Anime details as a dictionary
        """
        container = self.db_handler.get_container('anime_details_full')

        # Step 1: Query the database for the anime by name
        query = "SELECT * FROM c WHERE c.anime_name = @anime_name"
        parameters = [{"name": "@anime_name", "value": anime_name}]
        
        # Use the db_handler to run the query
        results = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        # Step 2: If anime is found, return the details
        if results:
            print(f"Anime '{anime_name}' found in database.")
            return results[0]  # Return the first matching result
        
        print(f"Anime '{anime_name}' not found in database. Fetching details from external source...")
        fetched_details = self.mal_fetcher.get_anime_details_from_name(anime_name)
        
        # Step 4: Insert the fetched details into the database
        if fetched_details:
            self.db_handler.write_anime_details(anime_name, fetched_details)
            return fetched_details
        
        # TO-DO: decide whether to make this an exception
        return None

if __name__ == '__main__':
    from Utils.MAL_connection.MAL_API_fetcher import MAL_API_Fetcher

    db_handler = DatabaseHandler('MalRecCosmos')
    fetcher = MAL_API_Fetcher()
    anime_service = AnimeRecommenderService(db_handler, fetcher)

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
    anime_name = 'Naruto'
    anime_details = fetcher.get_anime_details_from_name(anime_name)
    print((anime_details['id'], anime_details['title']))

    db_handler.write_anime_details(anime_name, anime_details)
    print("succesfully upserted my item")
    container = db_handler.get_container(container_id)
    # print(db_handler.read_item(container, '20', 'Naruto'))

    print(anime_service.get_anime_details('86'))

