# DnDBot

## Overview

Author: abomb2323

Version: 1.0

DnDBot is a discord bot for channels which run multiple DnD games, allowing for ease of use in organizing, reminding, and informing players.


## Installation

DnDBot is tested on Python 3.6.7, as Python 3.7 causes an error inside the discord.py library. If you are running into syntax errors, please run DnDBot on Python 3.6.7.

### Linux

*Tested on ArchLinux with Python 3.6.7*

**Step One**

Ensure that Python 3.6.7 and `pip` are installed, then run the following command:

`python3.6 -m pip install -U discord.py`

This installs the discord.py library, a wrapper for python to allow it to access the Discord API.


**Step Two**

Clone this repository using `git`:

`git clone https://github.com/abomb2323/DnDBot`

After it finishes, use `cd DnDBot` to navigate into the project folder.


**Step Three**

Add your bot's token into "config.json" where it says <INSERT_TOKEN>, making sure to replace the <> symbols.


**Step Four**

To run the bot, use the following command:

`python3.6 DnDBot.py`


### Windows

*Windows installation instructions will be added at a later time.


### Patch Notes
```
Patch Notes v1.0
* First release
* Added Blacklist and Whitelist feature to allow commands to not be acknowledged in certain channels.
* Added campaign role creation (mentionable)
* Added user addition and removal from campaign.
```