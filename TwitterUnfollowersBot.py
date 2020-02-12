#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Bot for displaying unfollowers for a Twitter account.

import time

from secrets import password
from secrets import username
from selenium import webdriver


TWITTER_LOGIN_URL = 'https://twitter.com/login'


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
        pass


def main():
    twitterbot = TwitterBot(username, password)

    # Test.
    time.sleep(5)


if __name__ == '__main__':
    main()
