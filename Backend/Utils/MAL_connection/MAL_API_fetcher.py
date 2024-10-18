import requests
import numpy as np
import time
import json
import os
# This class is used as the main application for collecting data from the myanimelist API

class AnimeIdNotFoundException(Exception):
   pass

class AnimeExactMatchNotFoundException(Exception):
   pass

class AnimeMatchNotFoundException(Exception):
   pass

class AnimeDetailsHTTPError:
   pass

class MAL_API_Fetcher:

  def __init__(self, API_connector):
    self.base_url = "https://api.myanimelist.net/v2/"
    self.file_dir  = os.path.dirname(__file__)
    # self.api_key = self.get_api_key()
    self.api_connector = API_connector
    self.access_token = self.api_connector.access_token

  # Function to get user anime list with scores
  def get_user_anime_list(self, username):

      # Endpoint to retrieve user anime list
      endpoint = f"users/{username}/animelist"

      # Parameters for filtering by score and pagination
      params = {
          "fields": "list_status,anime(id,title,score)",
          "status": "completed", # This will filter the results by only the completed anime
          "sort": "list_score",
          "limit": 300,  # Adjust the limit as needed
          "offset": 0,
      }
      # Initialize an empty list to store results
      user_anime_list = []

      while True:
          # Make the API request
          response = requests.get(
              f"{self.base_url}{endpoint}",
              params=params,
              headers={"Authorization": f"Bearer {self.access_token}"}
          )
          time.sleep(0.4)

          if response.status_code == 200:
              data = response.json()
              user_anime_list.extend(data["data"])
              break
          else:
              print(response.json())
              print(f"Error fetching anime list for {username}: {response.status_code}")
              break

      return user_anime_list

  # Function to filter users with more than 100 reviews and collect their lists
  def collect_user_lists(self, users, min_reviews=100):
      user_lists_with_scores = []

      # runtime metrics
      count = 0
      animelist_collection_times = []

      for user in users:
          start = time.time() # stats
          anime_list = self.get_user_anime_list(user)
          duration = time.time() - start
          animelist_collection_times.append(duration)
          if duration >= 1:
            print(f"Warning: {user}'s animelist took {duration} secs to be collected")

          if count%10 == 0:
            print(f"{count} users animelist collected")

          count += 1

          # Filter users with more than 100 reviews
          if len(anime_list) >= min_reviews:
              user_lists_with_scores.append({"username": user, "anime_list": anime_list})

          time.sleep(0.4)

      print(f"The mean duration was: {np.mean(np.array(animelist_collection_times))}")

      return user_lists_with_scores

  def get_anime_details_from_name(self, anime_name):
    anime_id, _ = self.get_anime_id(anime_name)
    anime_details = self.get_anime_details(anime_id)
    return anime_details
      
  # Function to search anime by name with exact match using MyAnimeList API
  def get_anime_id(self, anime_name):
      # The MAL API endpoint for searching anime by name
      url = f"https://api.myanimelist.net/v2/anime?q='{anime_name}'&limit=100"

      # Set up the headers with the access token for authorization
      headers = {
          "Authorization": f"Bearer {self.access_token}"
      }

      # Make the GET request to search for the anime
      response = requests.get(url, headers=headers)
      response.raise_for_status()
      # Check if the request was successful
      # Parse the JSON response
      data = response.json()
      if data.get('data'):
          # Loop through the results to find an exact match
          for anime in data['data']:                  
              if anime['node']['title'].lower() == anime_name.lower():
                  anime_id = anime['node']['id']
                  anime_title = anime['node']['title']
                  return anime_id, anime_title
          raise AnimeExactMatchNotFoundException(f"Got anime options for {anime_name}, but no exact match found.")
      else:
        raise AnimeMatchNotFoundException(f"No similar anime matches for {anime_name} were found")

  def get_anime_details(self, anime_id):
    # Base URL for getting anime details
    url = f"https://api.myanimelist.net/v2/anime/{anime_id}"
    
    # Fields we want to retrieve about the anime
    fields = (
        "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,"
        "popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,"
        "media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,"
        "source,average_episode_duration,rating,pictures,background,"
        "related_anime,related_manga,recommendations,studios,statistics"
    )

    headers = {
        "Authorization": f"Bearer {self.access_token}"
    }

    params = {
        "fields": fields
    }

    # Make the GET request to the API
    response = requests.get(url, headers=headers, params=params)
    try: 
      response.raise_for_status()
      return response.json()
    except requests.exceptions.HTTPError as e:
      raise AnimeDetailsHTTPError(f"Failed to get anime details from anime id {anime_id}: {e.message}")

if __name__ == '__main__':
  # Create Object
  from MAL_API_Connector import MAL_API_Connector
  class web_app_handler_test:
    def __init__(self):
        self.path = '.env'
        print(os.path.abspath(self.path))
    
    def update_app_setting(self, key, value):
        self.update_dotenv(key, value)
        print(f"Dummy updated key:{key} to value: {value}")

    def update_dotenv(self, key, new_value):
        """Updates or adds a key-value pair in the .env file"""
        env_vars = {}
        
        with open(self.path, 'r') as file:
            for line in file:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    env_vars[k] = v
        
        # Update or add the key-value pair
        env_vars[key] = new_value
        
        # Write the updated content back to the .env file
        with open(self.path, 'w') as file:
            for k, v in env_vars.items():
                file.write(f'{k}={v}\n')

  dummy_handler = web_app_handler_test()
  connector = MAL_API_Connector(dummy_handler)
  fetcher = MAL_API_Fetcher(connector)
  # print(fetcher.get_user_anime_list("TensaiOji"))

  # Example usage
  anime_name = "Naruto"
  anime_id, anime_title = fetcher.get_anime_id(anime_name)

  # anime_list = fetcher.get_anime_id(anime_name)
  # print(anime_list)

  if anime_id:
      print(f"Anime ID: {anime_id}, Title: {anime_title}")
  else:
      print(f"Error: {anime_title}")

  print(type(fetcher.get_anime_details_from_name(anime_name)))

# Class End
