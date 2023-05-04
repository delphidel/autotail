import requests
import json

url = 'https://api.guerrillamail.com/ajax.php'
op = 'get_email_address'
ip = '127.0.0.1'
agent = 'does_not_matter'

full_path = f'{url}?f={op}&ip={ip}&agent={agent}'


def main():
    print(f"Getting new address from {full_path}...")
    resp = requests.get(full_path)
    js = json.loads(resp.text)

    new_email = js['email_addr']
    print(new_email)

