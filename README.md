# DealBot
Experimental deal scraping bot in python using selenium.

# Scraping Deals on Telegram Channels using Selenium

## Requirements

1. install python and use *********pip********* to install the requirements using the ****************`requirements.txt`* file.

`pip install --no-cache-dir --upgrade -r requirements.txt`

1. Download Chrome web-driver for selenium and add the binary location to PATH
2. Edit the `[main.py](http://main.py)` file and change the “`query`" and “`tChannel`" variables to match your desired search query and channel to check.
3. Get your telegram bot token and save it in a file named `[keys.py](http://keys.py)` at the projects main directory. ************************************************inside the file, save the token in this format: `token = <YOUR_TOKEN_HERE>`**
4. On Telegram app, open your bot chat channel and write something. After that, run the `[bottest.py](http://bottest.py)` file with python to get your chat ID (it will be printed to the terminal).
5.  Edit the `[main.py](http://main.py)` file again, and change the value of the constant `CHATID` to your chat ID number that was shown in the last step.

## First Run

Once you successfully set-up your Telegram bot’s token, your chat ID, search query and channel to search in, run the `[main.py](http://main.py)` file. 

The first run will create some text files in the main project directory:

- A file containing all the messages found by the search, called `{your_query}.txt`
- A file containing all these message’s IDs, for comparison in the next runs (for update monitoring), called `{your_query}-ids.txt`
- A log file for the script execution.# Scraping Deals on Telegram Channels using Selenium

## Requirements

1. install python and use *********pip********* to install the requirements using the ****************`requirements.txt`* file.

`pip install --no-cache-dir --upgrade -r requirements.txt`

1. Download Chrome web-driver for selenium and add the binary location to PATH
2. Edit the `[main.py](http://main.py)` file and change the “`query`" and “`tChannel`" variables to match your desired search query and channel to check.
3. Get your telegram bot token and save it in a file named `[keys.py](http://keys.py)` at the projects main directory. ************************************************inside the file, save the token in this format: `token = <YOUR_TOKEN_HERE>`**
4. On Telegram app, open your bot chat channel and write something. After that, run the `[bottest.py](http://bottest.py)` file with python to get your chat ID (it will be printed to the terminal).
5.  Edit the `[main.py](http://main.py)` file again, and change the value of the constant `CHATID` to your chat ID number that was shown in the last step.

## First Run

Once you successfully set-up your Telegram bot’s token, your chat ID, search query and channel to search in, run the `[main.py](http://main.py)` file. 

The first run will create some text files in the main project directory:

- A file containing all the messages found by the search, called `{your_query}.txt`
- A file containing all these message’s IDs, for comparison in the next runs (for update monitoring), called `{your_query}-ids.txt`
- A log file for the script execution.

After the first run, every time the script is executed, the `*-ids.txt` file will be checked and compared with ids found in the current execution run. Every new message found will be forwarded to your bot chat channel.

After the first run, every time the script is executed, the `*-ids.txt` file will be checked and compared with ids found in the current execution run. Every new message found will be forwarded to your bot chat channel.
