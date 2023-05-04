import requests
import json
from pathlib import Path
from faker import Faker
import random
import openai


def main():
    story = (
        'Fuck off, scabs. I hope almost every "story" you get '
        "is from a Workers United ally."
    )
    email = make_email()

    print(email)

    story = write_story()

    print(story['choices'][0]['message']['content'])

    js = edit_template(make_email(), story)
    resp = post_story(js)

    print(resp)
    print(resp.text)


def make_email():
    faker = Faker()
    (first, last) = (faker.first_name(), faker.last_name())
    if random.randrange(0, 2) == 0:
        year = f"{random.randrange(0, 10)}{random.randrange(0, 10)}"
    else:
        decade = random.choice(["19", "20"])
        if decade == "19":
            year = f"{decade}{random.randrange(0, 10)}{random.randrange(0, 10)}"
        else:
            year = f"{decade}{random.randrange(0, 2)}{random.randrange(0, 10)}"
    sep = random.choice([".", "_", "-"])
    return f"{first}{sep}{last}{year}"


def write_story():
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "Please write in first person about a good experience with "
                    "the Starbucks union, Starbucks Workers United, in which either "
                    "your rights as an employee or your experience as a customer was "
                    "improved because the store was unionized."
                ),
            }
        ],
    )


def edit_template(email, story, path=Path(__file__).parent / "constants/template.json"):
    with open(path) as f:
        js = json.load(f)
        js["fields"]["3"]["value"] = story
        js["fields"]["10"]["value"] = email
        return js


def post_story(js, url="https://workersunitedfacts.com/wp/wp-admin/admin-ajax.php"):
    return requests.post(url, json=js)
