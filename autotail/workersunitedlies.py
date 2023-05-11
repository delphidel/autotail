from autotail.constants.locators import WorkersUnitedLiesLocator
from autotail.deployment import Deployment
from autotail.postbot import PostBot
import logging


class WorkersUnitedLiesPostbot(PostBot):
    def __postinit__(self):
        pass

    def post_story(self):
        """Abstract method implementation to post the story"""
        logging.debug("Posting story...")
        logging.debug(f"Have locator_dict: {self.locator_dict}")
        # Adding some mouse movement in to try to bypass recaptcha

        self.random_mouse_jitter(self.story_field)
        self.story_field.click()
        self.story_field.send_keys(self.story)
        self.random_sleep(0.25, 2)

        # only field guaranteed to be in bounds
        self.random_mouse_jitter(self.story_field)
        self.email_field.click()
        self.email_field.send_keys(self.email)
        self.random_sleep(0.25, 2)

        # only field guaranteed to be in bounds
        self.random_mouse_jitter(self.story_field)
        self.submit_button.click()

    def get_story(self):
        return self.story.replace("\n", "\\n") + "\n"


WorkersUnitedLiesDeployment = Deployment(
    name="workersunitedlies",
    urls=["https://workersunitedfacts.com/story/"],
    locators=dict(WorkersUnitedLiesLocator.__dict__),
    postbot=WorkersUnitedLiesPostbot,
)
