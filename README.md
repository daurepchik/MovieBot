# MovieBot

MovieBot is a Telegram bot that connects to a third-party API to show users information about movies in the top 250 movies according to IMDB. The bot also stores information about user commands, allowing users to view their last 10 entered commands.

## Installation

1. Python >= 3.9, pip and setuptools are required. Setuptools install with command:
```shell
pip install setuptools
```
2. Create [virtual environment](https://docs.python.org/3/library/venv.html) if necessary, then go to MovieBot root 
folder, install requirements, afterward run setup.py with following commands:
```shell
pip install -r requirements.txt
python setup.py install
```
3. In the MovieBot root folder copy the [.env.template](.env.template) file and name it `.env`.
4. Get your API host key:
   - Go to [Movies Database API host](https://rapidapi.com/SAdrian/api/moviesdatabase/)
   - copy `X-RapidAPI-Key` from the api header field 
   - put it to `.env` file's `SITE_API_KEY` field.
5. Get your Telegram API key:
   - Register your new telegram bot through [BotFather](https://t.me/BotFather)
   - Get your Telegram bot API there
   - Put it to `.env` file's `TELEGRAM_BOT_API_KEY` field.

## Usage

1. Activate your virtual environment (if configured), and run the `main.py` file:
```shell
python main.py
```
2. Start a chat with your MovieBot on Telegram.


## Authors

- [Dauren Aidenov](https://github.com/daurepchik) - Main Developer
- Alexander Mordvinov - SkillBox Curator

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).