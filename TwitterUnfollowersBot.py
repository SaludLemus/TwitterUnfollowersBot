#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Bot for displaying unfollowers for a Twitter account.

import time

from secrets import password
from secrets import username
from selenium import webdriver


TWITTER_LOGIN_URL = 'https://twitter.com/login'

LOAD_TIME = 4

#------------------------
# Used for the login page.
XPATH_USERNAME_INPUT = '//input[@name="session[username_or_email]"]'
XPATH_PASSWORD_INPUT = '//input[@name="session[password]"]'
XPATH_LOGIN = '//div[@role="button"]'
#------------------------


class TwitterBot:
    def __init__(self, username, password):
        """Initializes the bot with user's credentials."""

        self.username = username
        self.password = password

        # Open a Chrome browser and display the Twitter login page.
        self.driver = webdriver.Chrome()
        self.driver.get(TWITTER_LOGIN_URL)

    def SignIn(self):
        """Signs into the user's account via the page loaded by `__init__()`."""

        # Input the user's username/email.
        self.driver.find_element_by_xpath(
                XPATH_USERNAME_INPUT).send_keys(self.username)

        time.sleep(LOAD_TIME)

        # Input the user's password.
        self.driver.find_element_by_xpath(
                XPATH_PASSWORD_INPUT).send_keys(self.password)

        # Now, the `Log in` button should be clickable to actually sign into the
        # account.
        self.driver.find_element_by_xpath(XPATH_LOGIN).click()


def main():
    twitterbot = TwitterBot(username, password)

    # Let the page load fully, otherwise, an exception can occur.
    time.sleep(LOAD_TIME)

    twitterbot.SignIn()

    # Test.
    time.sleep(LOAD_TIME)


if __name__ == '__main__':
    main()
