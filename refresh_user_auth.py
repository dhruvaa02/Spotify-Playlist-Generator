import webbrowser
import secretinfo as si
import requests
import urllib
import base64
import json

"""Only provides refreshable user authentication for the modify-private scope!"""

def parse_url_param(url: str, param: str) -> str:

    "Parse param in url"

    query = urllib.parse.urlparse(url).query
    code = urllib.parse.parse_qs(query).get(param, None)

    return code[0]


def parse_code_from_url(url: str) -> str:

    "Parse URL with parameter 'code'"

    return parse_url_param(url, 'code')


def token_request(rbp: dict, auth: bool) -> any:
    
    if auth:
        oauth_url = 'https://accounts.spotify.com/api/token'
        creds = si.my_client_id + ':' + si.my_client_secret
        token = base64.b64encode(creds.encode())
        decoded = token.decode()
        headers = {'Authorization': f'Basic {decoded}'}
    
    final_token = requests.post(oauth_url, data=rbp, headers=headers)
    
    return final_token


def request_user_token(code: str) -> any:

    "Request a new user token"

    data = {'grant_type': "authorization_code", 'code': code, 'redirect_uri': 'https://google.com/'} 

    return token_request(rbp=data, auth = True)


def request_token(url: str) -> any:
    
    code = parse_code_from_url(url)

    return request_user_token(code)


def get_user_auth() -> any:

    #Client facing input
    webbrowser.open(si.auth_url)
    redirected = input('Please paste redirect URL: ').strip()

    #Using code for auth token

    final_request = request_token(url=redirected)
    return final_request.json()['access_token']


if __name__ == "__main__":
    get_user_auth()