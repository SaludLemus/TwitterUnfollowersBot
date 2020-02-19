# Twitter Unfollowers Bot

## Requirements

#### Selenium Python Module
Install the module via `pip3` as such: `pip3 install selenium`
* __NOTE:__ Would recommend installing the module under a virtual environment to avoid module conflicts.

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
1. The Python3 script imports the `username` variable and `password` variable from a `secrets.py` file, so this Python file should be defined in the same directory as the `TwitterUnfollowersBot.py` file:<br />
<a href="https://ibb.co/5cVPFGP"><img src="https://i.ibb.co/PC8dQFd/secrets-file.png" alt="secrets-file" border="0"></a><br />
2. Both `username` and `password` variables are strings, where `username` is your username to log onto Twitter and `password` is the password to your Twitter account:<br />
<a href="https://ibb.co/yNDZZvH"><img src="https://i.ibb.co/BfmQQW0/secrets-info.png" alt="secrets-info" border="0"></a><br />
