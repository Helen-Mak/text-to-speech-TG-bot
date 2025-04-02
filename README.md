# Text-to-Speech Telegram Bot  

A Telegram bot that converts text messages into voice messages. The bot provides language selection and supports text-to-speech conversion in English, German, and Russian.  

## Features  
- Converts text messages into voice messages  
- Supports three languages: English, German, and Russian  
- Provides an initial language selection menu  
- Uses Google Text-to-Speech (gTTS) for audio generation  

## Installation  
1. Clone this repository:  
   ```bash
   git clone https://github.com/Helen-Mak/text-to-speech-TG-bot.git

2. Install dependencies:
    pip install -r requirements.txt

3. Create a config.py file and add your bot token:
    TOKEN = "your-telegram-bot-token"

4. Run the bot:
    python main.py

## Usage

1. Start the bot by sending the /start command.

2. Select the language for text-to-speech conversion.

3. Send a text message, and the bot will generate a voice message in the selected language.

## Technologies
- Python 3.11+
- Aiogram 3.0
- gTTS (Google Text-to-Speech)
- Telegram Bot API

```md
## License  
This project is licensed under the MIT License. See the LICENSE file for details. 