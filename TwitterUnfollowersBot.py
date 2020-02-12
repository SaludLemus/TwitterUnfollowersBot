#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Bot for displaying unfollowers for a Twitter account.

import os
import secrets
import selenium
import time

from secrets import password
from secrets import username
from selenium import webdriver


TWITTER_LOGIN_URL = 'https://twitter.com/login'

# How long to wait for the page to load (in seconds).
LOAD_TIME = 4

#--------------------------------------------------------------------
# Used for the login page.
XPATH_USERNAME_INPUT = '//input[@name="session[username_or_email]"]'
XPATH_PASSWORD_INPUT = '//input[@name="session[password]"]'
XPATH_LOGIN_BUTTON = '//div[@role="button"]'
XPATH_INVALID_CREDENTIALS = ('//span[contains(text(),'
        '"did not match our records")]')
XPATH_UNUSUAL_ACTIVITY = '//span[contains(text(), "unusual login activity")]'
XPATH_CAPTCHA_CHALLENGE = ('//span[contains(text(),'
        '"confirm you’re not a robot")]')
#--------------------------------------------------------------------


#--------------------------------------------------------------------
# Used to go to a user's Twitter profile page.
XPATH_USER_PROFILE = '//a[@href="/%s"]' % username
#--------------------------------------------------------------------


class TwitterBot:
    def __init__(self, username, password):
        """Initializes the bot with user's credentials."""

        self.username = username
        self.password = password

        # Open a Chrome browser and display the Twitter login page.
        self.driver = webdriver.Chrome()
        self.driver.get(TWITTER_LOGIN_URL)

        # Wait for the login page to load fully.
        time.sleep(LOAD_TIME)

        self._SignIn()

    def _SignIn(self):
        """Signs into the user's account via the page loaded by `__init__()`."""

        # Input the user's username/email.
        self.driver.find_element_by_xpath(
                XPATH_USERNAME_INPUT).send_keys(self.username)

        # Input the user's password.
        self.driver.find_element_by_xpath(
                XPATH_PASSWORD_INPUT).send_keys(self.password)

        # Now, the `Log in` button should be clickable to actually sign into the
        # account.
        self.driver.find_element_by_xpath(XPATH_LOGIN_BUTTON).click()

        # Once signed in, the user is taken to their home feed, so depending on
        # the user's feed, it can take a while to fully load.
        time.sleep(LOAD_TIME * 2)

        # Verify that the login was successful by finding specific text on a
        # wrong sign in attempt.
        try:
            self.driver.find_element_by_xpath(XPATH_INVALID_CREDENTIALS)

            self.driver.quit()
            raise ValueError('Invalid username or password, please correct it.')
        except selenium.common.exceptions.NoSuchElementException:
            try:
                self.driver.find_element_by_xpath(XPATH_UNUSUAL_ACTIVITY)

                self.driver.quit()
                raise ValueError('Invalid username or password, '
                        'please correct it.')
            except selenium.common.exceptions.NoSuchElementException:
                try:
                    # Twitter may make the user solve a reCAPTCHA challenge
                    # which this program does not support.
                    self.driver.find_element_by_xpath(XPATH_CAPTCHA_CHALLENGE)

                    self.driver.quit()
                    raise ValueError('Program does not support solving a '
                            'reCAPTCHA challenge.')
                except selenium.common.exceptions.NoSuchElementException:
                    pass

        # Successfully logged in.

    def GoToUserTwitterProfile(self):
        """Navigates to the user's Twitter profile."""

        self.driver.find_element_by_xpath(XPATH_USER_PROFILE).click()

        # Similar to waiting for the home feed to load, it also applies to the
        # user's profile page.
        time.sleep(LOAD_TIME * 2)


def main():
    """Creates the Twitter bot."""

    global username
    global password
    # The Twitter login page requires at least 1 character for `username` and
    # `password` in order for the `Log in` button to be clickable.
    if not username:
        raise ValueError('Did not specify a username, please go to %s '
                'and add it.' % os.path.abspath(secrets.__file__))
    
    if not password:
        raise ValueError('Did not specify a password, please got to %s '
                'and add it.' % os.path.abspath(secrets.__file__))

    username = 'a@gmail.com'
    password = 'some'
    twitterbot = TwitterBot(username, password)

    time.sleep(LOAD_TIME)

    twitterbot.GoToUserTwitterProfile()


if __name__ == '__main__':
    main()
