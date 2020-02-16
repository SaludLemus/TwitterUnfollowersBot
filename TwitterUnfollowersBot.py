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
        #user_cells = users_timeline.find_elements_by_xpath(XPATH_USER_CELLS)

        at_set = set()

        # Base case where the user has no followers/following.
        try:
            users_timeline.find_element_by_xpath(XPATH_USER_CELLS)
        except selenium.common.exceptions.NoSuchElementException:
            return at_set

        # 1 is a placeholder.
        user = 1
        while user:
            # Get all possible user cells.
            user_cells = users_timeline.find_elements_by_xpath(XPATH_USER_CELLS)

            # Perform binary search on the resulted list in `user_cells` to find
            # the last instance of a added user cell -> store its index in
            # `start`.
            start = None

            # For debugging purposes.
            #print('Length of search space: %d' % len(user_cells))

            # Starting positions are 0 index and last index of the returned
            # list.
            left = 0
            right = len(user_cells) - 1 
            while left <= right:
                mid = int((left + right) / 2)

                # For debugging purposes.
                #print('Midpoint: %d' % mid)

                # `href` attribute returns link/URL of the user.
                # Ex: https://twitter.com/SOME_USER
                cur_user = user_cells[mid].find_element_by_tag_name(
                        'a').get_attribute('href').split('/')[-1]

                # For debugging purposes.
                #print('Cur user in search space: %s' % cur_user)
                #print('Cur @ set: ', at_set)

                # Current user is in the added user set, so every user before it
                # has been added (if previous users exist/this user is not the
                # first in the list), so search the right side.
                if cur_user in at_set:
                    # For debugging purposes.
                    #print('User in set, so searching right side or term.')

                    # Exhausted all search space, so the next index (`left + 1`)
                    # is the next user to be added.
                    if left == right:
                        start = left + 1
                        break

                    # Still have not exhausted all search space, so search the
                    # right side.
                    left = mid + 1
                else:
                    # For debugging purposes.
                    #print('User not in set, so searching left side or term.')

                    # Current user has not been added to the set, so search the
                    # left side.
                    
                    # Exhausted all search space, so `left` is the index for the
                    # next user to be added.
                    if left == right:
                        start = left
                        break

                    # Not exhausted all search space, so search left side.
                    right = mid - 1

            if left > right:
                start = left
            
            # For debugging purposes.
            #print('Start: ', start)

            assert type(start) == int, ('Did not initialize `start` index to '
                    'add users.')

            # For debugging purposes.
            #print('start idx: %d' % start)

            # 0 is a placeholder.
            user = 0
            # Now add all unadded users from `start` to `len(user_cells)`.
            for i in range(start, len(user_cells)):
                cur_user = user_cells[i]
                
                cur_user_at = cur_user.find_element_by_tag_name(
                        'a').get_attribute('href').split('/')[-1]

                # For debugging purposes.
                #print(cur_user_at)

                assert cur_user_at not in at_set, ('Attempting to add an '
                        'existing user (e.g. %s) to set.' % cur_user_at)

                at_set.add(cur_user_at)

                user = cur_user

            # Found all users in followers/following.
            if not user:
                break

            # Scroll to the last user added.
            self.driver.execute_script('arguments[0].scrollIntoView(true);',
                    user)

            # Wait for nearby users to fully load.
            time.sleep(LOAD_TIME)

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

    def _PrintUnfollowers(self, unfollowers):
        """Prints all the unfollowers to stdout."""

        if not unfollowers:
            print('All people that you follow, follow you back.')
            return

        print('Here is the list of people (their @) that are NOT following '
                'you:')

        for unfollower in unfollowers:
            print(unfollower)

    def GetUnfollowers(self):
        """Returns a list of all unfollowers for the user."""

        self.GoToUserTwitterProfile()

        user_following_set = self.GetUserFollowing()

        self.GoToUserTwitterProfile()

        user_followers_set = self.GetUserFollowers()

        # Considered "not following" if that user is in the "following" set but
        # not in the "followers" set.
        unfollowers = []
        for following in user_following_set:
            if following not in user_followers_set:
                unfollowers.append(following)

        # Let the user know of all its unfollowers.
        self._PrintUnfollowers(unfollowers)

        return unfollowers


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

    unfollowers = twitterbot.GetUnfollowers()


if __name__ == '__main__':
    main()
