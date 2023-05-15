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

        self.random_mouse_jitter(self.email_field)
        self.email_field.click()
        self.email_field.send_keys(self.email)
        self.random_sleep(0.25, 2)

        self.random_mouse_jitter(self.submit_button)
        logging.info("Clicking submit...")
        self.submit_button.click()
        self.random_sleep(1, 2)

        try:
            if self.error_msg != "":
                logging.error("Bad news! Got recaptcha'd.")
                logging.error(self.error_msg.text)
                raise RecaptchaError(self.error_msg.text)
        except AttributeError:
            logging.info("Looks like no error is present!")

    def get_story(self):
        return self.story.replace("\n", "\\n") + "\n"


WorkersUnitedLiesDeployment = Deployment(
    name="workersunitedlies",
    urls=["https://workersunitedfacts.com/story/"],
    locators=dict(WorkersUnitedLiesLocator.__dict__),
    postbot=WorkersUnitedLiesPostbot,
)


class RecaptchaError(Exception):
    """Exception for recaptcha"""
