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

#--------------------------------------------------------------------
# Used to navigate to the user's followers and following.
XPATH_USER_FOLLOWERS = '//a[@href="/%s/followers"]' % username
XPATH_USER_FOLLOWING = '//a[@href="/%s/following"]' % username
#--------------------------------------------------------------------

#--------------------------------------------------------------------
# Used to obtain the list of following.
XPATH_FOLLOWING_TIMELINE = '//div[@aria-label="Timeline: Following"]'
#--------------------------------------------------------------------

#--------------------------------------------------------------------
# Used to obtain the list of followers.
XPATH_FOLLOWERS_TIMELINE = '//div[@aria-label="Timeline: Followers"]'
#--------------------------------------------------------------------


#--------------------------------------------------------------------
# Used to obtain either following or followers user cells.
XPATH_USER_CELLS = './/div[@data-testid="UserCell"]'
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

    def _GoToUserFollowers(self):
        """Navigates to the user's followers."""

        self.driver.find_element_by_xpath(XPATH_USER_FOLLOWERS).click()

        time.sleep(LOAD_TIME * 2)

    def _GoToUserFollowing(self):
        """Navigates to the user's following."""

        self.driver.find_element_by_xpath(XPATH_USER_FOLLOWING).click()

        time.sleep(LOAD_TIME * 2)

    def _GetAtSet(self, users_timeline):
        """Returns a set containing all unique @ following/followers.

        Args:
          users_timeline: The timeline that either contains all following or all
          followers.
        
        """
        
        user_cells = users_timeline.find_elements_by_xpath(XPATH_USER_CELLS)

        at_set = set()

        for cell in user_cells:
            at = cell.find_element_by_tag_name('a').get_attribute('href')

            at_set.add('@%s' % at.split('/')[-1])

        return at_set

    def GetUserFollowers(self):
        """Returns a list of the user's followers."""

        self._GoToUserFollowers()

        followers_timeline = self.driver.find_element_by_xpath(
                XPATH_FOLLOWERS_TIMELINE)

        return self._GetAtSet(followers_timeline)

    def GetUserFollowing(self):
        """Returns a list of the user's following."""

        self._GoToUserFollowing()

        following_timeline = self.driver.find_element_by_xpath(
                XPATH_FOLLOWING_TIMELINE)

        return self._GetAtSet(following_timeline)


def main():
    """Creates the Twitter bot."""

    # The Twitter login page requires at least 1 character for `username` and
    # `password` in order for the `Log in` button to be clickable.
    if not username:
        raise ValueError('Did not specify a username, please go to %s '
                'and add it.' % os.path.abspath(secrets.__file__))
    
    if not password:
        raise ValueError('Did not specify a password, please got to %s '
                'and add it.' % os.path.abspath(secrets.__file__))

    twitterbot = TwitterBot(username, password)

    twitterbot.GoToUserTwitterProfile()

    user_following_set = twitterbot.GetUserFollowing()

    twitterbot.GoToUserTwitterProfile()

    user_followers_set = twitterbot.GetUserFollowers()

    # Considered "not following" if that user is in the "following" set but not
    # in the "followers" set.
    unfollowers = []
    for following in user_following_set:
        if following not in user_followers_set:
            unfollowers.append(following)

    # Verify that the user does have unfollowers.
    if unfollowers:
        print('Here is the list of people (their @) that '
                'are NOT following you:')

        for unfollower in unfollowers:
            print(unfollower)


if __name__ == '__main__':
    main()
