import typing
from dataclasses import dataclass
import random
import logging

import openai
from faker import Faker

from autotail.postbot import PostBot


@dataclass
class Deployment:
    name: str
    urls: typing.List[str]
    locators: typing.Dict[str, typing.Tuple[str, str]]
    """
    Dictionary of locators using selenium.webdriver.common.By classes like::
    
        {
            'locator_name': (By.<LOCATOR_TYPE>, 'locator')
        }
    """
    postbot: typing.Type[PostBot]
    """
    A subclass of PostBot for this particular deployment that implements an apply method
    """

    deployments: typing.ClassVar = []

    def make(self, **kwargs) -> PostBot:
        """
        Instantiate a PostBot with a url chosen at random,
        passing **kwargs onto the PostBot
        """
        url = random.choice(self.urls)
        logging.info(f"Url: {url}")
        self.email = self.make_email()
        logging.info(f"Generated email: {self.email}")
        self.story = self.write_story()
        logging.info(f"Retrieved story: {self.story}")
        return self.postbot(
            url=url,
            locator_dict=self.locators,
            email=self.email,
            story=self.story,
            **kwargs,
        )

    def __post_init__(self):
        self.deployments.append(self)

    @classmethod
    def get_deployments(cls) -> typing.Dict[str, "Deployment"]:
        """
        Return a dictionary of declared Deployment objects, with their `name`s as keys
        """
        deploys = {deploy.name: deploy for deploy in cls.deployments}
        return deploys

    def make_email(self):
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

    def write_story(self):
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Please tell me a very short story in first person about an experience with "
                        "the Starbucks union, Starbucks Workers United, in which either "
                        "one's rights as an employee or one's experience as a customer was "
                        "improved because the store was unionized."
                    ),
                }
            ],
        )

        return resp["choices"][0]["message"]["content"]
