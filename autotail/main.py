import requests
import json
from pathlib import Path


def main():
    story = (
        'Fuck off, scabs. I hope almost every "story" you get '
        'is from a Workers United ally.'
    )
    js = edit_template('rebecca.portia66@gmail.com', story)

    resp = post_story(js)

    print(resp)
    print(resp.text)


# TODO: rewrite to generate an address @gmail.com
def get_email(url='https://api.guerrillamail.com/ajax.php',
              ip='127.0.0.1',
              user_agent='does_not_matter'):
    full_path = f'{url}?f=get_email_address&ip={ip}&agent={user_agent}'

    resp = requests.get(full_path)
    js = json.loads(resp.text)
    return js['email_addr']


def edit_template(email,
                  story,
                  path=Path(__file__).parent / 'constants/template.json'):
    with open(path) as f:
        js = json.load(f)
        print(js['fields'])
        js['fields']['3']['value'] = story
        js['fields']['10']['value'] = email
        return js
        

def post_story(js,
               url='https://workersunitedfacts.com/wp/wp-admin/admin-ajax.php'):
    return requests.post(url, json=js)
    
