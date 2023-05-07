import typing
from dataclasses import dataclass
import random
import logging

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
        logging.info("Using position url: {}".format(url))
        return self.postbot(url=url, locator_dict=self.locators, **kwargs)

    def __post_init__(self):
        self.deployments.append(self)

    @classmethod
    def get_deployments(cls) -> typing.Dict[str, 'Deployment']:
        """
        Return a dictionary of declared Deployment objects, with their `name`s as keys
        """
        deploys = {deploy.name: deploy for deploy in cls.deployments}
        return deploys
