# Twitter Unfollowers Bot

The purpose of this script is to automate the process of determining all unfollowers on your Twitter account (i.e. all unfollowers that fall under "Following"). Yes, I know that Twitter has a "Follows you" text right next to a Twitter user's "@", so this script takes advantage of that feature.

## Requirements

#### Selenium Python Module
Install the module via `pip3` as such: `pip3 install selenium`
* __NOTE:__ Would recommend installing the module in a virtual environment to avoid module conflicts.

#### Chrome Webdriver 
1. Determine the version of Google Chrome that you're using via `chrome://settings/help` (paste into the search bar):<br />
<a href="https://ibb.co/26cKSPt"><img src="https://i.ibb.co/Jdrkq27/Chrome-Version.png" alt="Chrome-Version" border="0"></a><br />

2. Then go to https://chromedriver.chromium.org/downloads:<br />
<a href="https://ibb.co/0ygcDBS"><img src="https://i.ibb.co/Qv2fb8R/Chrome-Driver-Version.png" alt="Chrome-Driver-Version" border="0"></a><br />
And find your browser version listed and click on it (if the version is not listed, then update Chrome):<br />
<a href="https://ibb.co/2Zgjw0C"><img src="https://i.ibb.co/mN6Hmr2/Chrome-Version-Zip-Files.png" alt="Chrome-Version-Zip-Files" border="0"></a><br />
Then download the appropriate `.zip` file according to your OS.

3. Unzip the `.zip` file and move the  `chromedriver` file:<br />
<a href="https://ibb.co/g6Txf95"><img src="https://i.ibb.co/yVyrZPw/Chrome-Driver-File.png" alt="Chrome-Driver-File" border="0"></a><br />
into the `/usr/local/bin` directory:<br />
<a href="https://imgbb.com/"><img src="https://i.ibb.co/xhwj9j7/chromedriver-file-new-location.png" alt="chromedriver-file-new-location" border="0"></a><br />

#### `secrets.py` file
1. The Python3 script imports the `username` variable and `password` variable from a `secrets.py` file, so this Python file should be defined/created/added in the same directory as the `TwitterUnfollowersBot.py` file like below:<br />
<a href="https://ibb.co/5cVPFGP"><img src="https://i.ibb.co/PC8dQFd/secrets-file.png" alt="secrets-file" border="0"></a><br />
2. Both `username` and `password` variables are strings, where `username` is your username to log onto Twitter and `password` is the password to your Twitter account, so using your favorite editor, fill in that information for the `secrets.py` file like below (inbetween each of the " "):<br />
<a href="https://ibb.co/yNDZZvH"><img src="https://i.ibb.co/BfmQQW0/secrets-info.png" alt="secrets-info" border="0"></a><br />

## Execution of `TwitterUnfollowersBot.py` file
Using your terminal, go to the directory/path where `TwitterUnfollowersBot.py` lives and execute the file as: `./TwitterUnfollowersBot.py`

## A few NOTES
1. This script assumes that there is NO additional step to "sign in" after inputting your username and password such as Two Factor Authentication (2FA) on your account; otherwise, the script will fail.
2. The script will fail if either the username or password is wrong.
3. Do NOT interact with the automated web browser (e.g. clicking on links, etc.), so let the script do its thing; otherwise, an error will happen (i.e. some elements will not be found because a different page was loaded).
4. The output of the script is sent to stdout (gets displayed on the terminal), where each row represents a Twitter user that is NOT following you (its their "@", along with their Twitter profile URL which is clickable and it takes you to their profile) like below:<br />
<a href="https://ibb.co/PTY6MQs"><img src="https://i.ibb.co/6vZW8Bc/Twitter-unfollowers-example.png" alt="Twitter-unfollowers-example" border="0"></a><br />
<a href="https://ibb.co/j6pDdzV"><img src="https://i.ibb.co/gjnJGdv/Twitter-unfollowers-example-2.png" alt="Twitter-unfollowers-example-2" border="0"></a><br />
5. The script takes a while (look at the execution time at the above picture) because the script needs to wait for a page to load (to ensure that the elements are loaded) and this is dependent on your internet connection, so if the script fails because a page took too long to load, you can modify the `LOAD_TIME` variable or modify each statement that is `time.sleep()` (both are found in the `TwitterUnfollowersBot.py` file) according to your needs.
6. At any point, if the scripts fails (e.g. exceptions, etc. which will populate the terminal), then it is okay to click the 'X' to exit the automated Chrome browser. :sweat_smile:
7. If everything goes well, then your unfollowers will get displayed to stdout, and the Chrome browser will close by itself.
