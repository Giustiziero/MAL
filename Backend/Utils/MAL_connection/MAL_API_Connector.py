from dotenv import load_dotenv
import os
import json
import requests

class AccessTokenBrokenException(Exception):
    pass

# This class has the responsibility of fetching information from our Anime information source, which is the myanimelist API
# We have the assumption of already having a token.json file in the same directory
class MAL_API_Connector:
    def __init__(self):
        load_dotenv()
        self.file_dir = os.path.dirname(__file__)
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.refresh_token = self.get_refresh_token()
        self.access_token = self.get_access_token()

    def get_refresh_token(self):
        with open(f'{self.file_dir}/token.json', "r") as f:
            token = json.load(f)
            return token['refresh_token']

    def get_access_token(self):
        with open(f'{self.file_dir}/token.json', "r") as f:
            token = json.load(f)
            if self.test_access_token(token['access_token']):
                return token['access_token']
            else:
                token = self.activate_refresh_token()
                if self.test_access_token(token):
                    return token
                else:
                    raise AccessTokenBrokenException(f"Even after refreshing we couldn't connect to the API")

    def test_access_token(self, access_token):
        try: 
            self.print_user_info(access_token)
            print("returned True")
            return True
        except requests.exceptions.HTTPError as err:
            print(f"Access token did not work: {err}")
            return False

    def print_user_info(self, access_token: str):
        url = 'https://api.myanimelist.net/v2/users/@me'
        response = requests.get(url, headers = {
            'Authorization': f'Bearer {access_token}'
            })
        response.raise_for_status()
        user = response.json()
        response.close()
        print(f"\n>>> Greetings {user['name']}! <<<")

    def activate_refresh_token(self):
            url = 'https://myanimelist.net/v1/oauth2/token'
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': f"{self.refresh_token}"
            }
            print(data)

            response = requests.post(url, data)
            response.raise_for_status()  # Check whether the request contains errors

            token = response.json()
            response.close()
            print('Token generated successfully!')

            with open(f'{self.file_dir}/token.json', 'w') as file:
                json.dump(token, file, indent = 4)
                print('Token saved in "token.json"')
            return token

if __name__ == '__main__':
    new_connector = MAL_API_Connector()

