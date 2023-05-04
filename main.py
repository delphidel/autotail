import requests

url = "https://api.guerillamail.com/ajax.php"
op = "get_email_address"
ip = "127.0.0.1"
agent = "made_up_fake"

full_path = f"{url}?f={op}&ip={ip}&agent={agent}"

print(full_path)

resp = requests.get(full_path)

print(resp)
