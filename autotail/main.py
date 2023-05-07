import logging
from faker import Faker
import random
import openai
from autotail.workersunitedlies import WorkersUnitedLiesDeployment
import sys
import time

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    story = (
        'Fuck off, scabs. I hope almost every "story" you get '
        "is from a Workers United ally."
    )
    email = make_email()

    logging.info(f"email: {email}")

    # story = write_story()

    logging.info(f"story: {story}")

    deployment = WorkersUnitedLiesDeployment

    bot = deployment.make(headless=False, email=email, story=story)
    bot.post_story()
    bot.quit()

    logging.info("Success!")

    # js = edit_template(make_email(), story)
    # resp = post_story(js)

    # logging.info(f"resp code: {resp}")
    # logging.info(f"resp body: {resp.text}")


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
    return f"{first}{sep}{last}{year}@gmail.com"


def write_story():
    resp = openai.ChatCompletion.create(
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

    return resp['choices'][0]['message']['content']
