import requests
import numpy as np
import time
import json
import MAL_API_Connector

# This class is used as the main application for collecting data from the myanimelist API

class MAL_API_Fetcher:

  def __init__(self):
    self.base_url = "https://api.myanimelist.net/v2/"
    self.api_key = self.get_api_key()
    self.api_connector = MAL_API_Connector()
    self.api_token = self.api_connector.access_token

  def get_api_key(self):
    with open('token.json', "r") as f:
      json_file = json.load(f)
      access_token = json_file['access_token']
    return access_token

  # Function to get user anime list with scores
  def get_user_anime_list(self, username):

      # username = "TensaiOji"

      # url = f'https://api.myanimelist.net/v2/users/{username}/animelist'
      # url_2 = f'https://api.myanimelist.net/v2/users/{username}/animelist?fields=anime_list_entries.list_status.num_times_rewatched,score'

      # # Set up the headers with your access token
      # headers = {
      #     'Authorization': f'Bearer {access_token}',
      # }

      # # Send a GET request to retrieve the user's anime list
      # response = requests.get(url_2, headers=headers)



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
      # pdb.set_trace()
      # Initialize an empty list to store results
      user_anime_list = []

      while True:
          # Make the API request
          response = requests.get(
              f"{self.BASE_URL}{endpoint}",
              params=params,
              headers={"Authorization": f"Bearer {self.api_key}"}
          )
          time.sleep(0.4)

          if response.status_code == 200:
              data = response.json()
              user_anime_list.extend(data["data"])
              break
              # Check if there are more pages
              # if "paging" in data and "next" in data["paging"]:
              #     params["offset"] += 300
              #     pdb.set_trace()
              # else:
              #     break
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


# Class End
