from selenium.webdriver.common.by import By


class WorkersUnitedLiesLocator:
    story_field = (By.ID, "nf-field-3")
    email_field = (By.ID, "nf-field-10")
    submit_button = (By.ID, "nf-field-4")
    error_msg = (By.CLASS_NAME, "nf-error-recaptcha")


class RecaptchaTestLocator:
    field_a = (By.NAME, "ex-a")
    field_b = (By.NAME, "ex-b")
    submit_button = (By.CLASS_NAME, "g-recaptcha")
