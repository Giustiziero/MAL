#!/usr/bin/bash/env python

import secrets
import json
import requests
import os
from dotenv import load_dotenv
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]

code_verifier = code_challenge = get_new_code_verifier()

print(len(code_verifier))
print(code_verifier)

# Get the current working directory
current_directory = os.getcwd()

# Display the current working directory
print("Current Directory:", current_directory)

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# 1. Generate a new Code Verifier / Code Challenge.
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]

# 2. Print the URL needed to authorise your application.
def print_new_authorisation_url(code_challenge: str):
    global CLIENT_ID

    url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&code_challenge={code_challenge}'
    print(f'Authorise your application by clicking here: {url}\n')

# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token(authorisation_code: str, code_verifier: str) -> dict:
    global CLIENT_ID, CLIENT_SECRET

    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': authorisation_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the request contains errors

    token = response.json()
    response.close()
    print('Token generated successfully!')

    token_path = os.path.dirname(__file__)
    with open(f'{token_path}/token.json', 'w') as file:
        json.dump(token, file, indent = 4)
        print('Token saved in "token.json"')

    return token

# 4. Test the API by requesting your profile information
def print_user_info(access_token: str):
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers = {
        'Authorization': f'Bearer {access_token}'
        })
    response.raise_for_status()
    user = response.json()
    response.close()
    print(f"\n>>> Greetings {user['name']}! <<<")

def refresh_token(refresh_token: str):
    global CLIENT_ID, CLIENT_SECRET

    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': f"{refresh_token}"
    }
    print(data)
    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the request contains errors

    token = response.json()
    response.close()
    print('Token generated successfully!')

    cur_dir = os.path.dirname(__file__)
    with open(f'{cur_dir}/token.json', 'w') as file:
        json.dump(token, file, indent = 4)
        print('Token saved in "token.json"')

    return token

if __name__ == '__main__':
    code_verifier = code_challenge = get_new_code_verifier()
    # print_new_authorisation_url(code_challenge)
    # print(current_directory)
    # authorisation_code = input('Copy-paste the Authorisation Code: ').strip()
    # token = generate_new_token(authorisation_code, code_verifier)
    
    # print(refresh_token(REFRESH_TOKEN_NUM))
    cur_dir = os.path.dirname(__file__)
    with open(f'{cur_dir}/token.json', "r") as f:
        token = json.load(f)
        print(refresh_token(token['refresh_token']))

    # print(token)
    
    # print_user_info(token['access_token'])