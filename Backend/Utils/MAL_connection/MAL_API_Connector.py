from dotenv import load_dotenv
import os
import json
import requests
# from .azure_web_app_handler import AzureWebAppHandler

class AccessTokenBrokenException(Exception):
    pass

# This class has the responsibility of fetching information from our Anime information source, which is the myanimelist API
# We have the assumption of already having a token.json file in the same directory
class MAL_API_Connector:
    def __init__(self, web_app_handler):
        load_dotenv()
        self.file_dir = os.path.dirname(__file__)
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.refresh_token = os.getenv('REFRESH_TOKEN')
        self.env_handler = web_app_handler
        self.access_token = self.get_access_token()

    def get_access_token(self):
        access_token = os.getenv('ACCESS_TOKEN')
        if self.test_access_token(access_token):
            return access_token
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

            self.env_handler.update_app_setting('ACCESS_TOKEN', token['access_token'])
            self.env_handler.update_app_setting('REFRESH_TOKEN', token['refresh_token'])
            print('Token saved in environment handler')
            return token['access_token']

if __name__ == '__main__':
    load_dotenv()

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

    web_app_handler = web_app_handler_test()
    new_connector = MAL_API_Connector(web_app_handler)

    # new_connector.activate_refresh_token