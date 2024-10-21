# AutoScout Car Listings Bot

This project is an educational bot designed to scrape and monitor new car listings from AutoScout24. It extracts information such as make, model, price, transmission type, fuel type, and other key details about the cars, then stores this data in a database for further use.

**Important:** This project is strictly for educational purposes. The responsibility for how this code is used lies entirely with the user. The authors of this project do not assume any liability for misuse or any damages arising from the use of this code.

## Features

- Fetches and processes new car listings from [AutoScout24](https://www.autoscout24.de).
- Extracts key details such as price, make, model, year, fuel type, transmission, CO2 emissions, and more.
- Saves car details into a database.
- Deletes outdated car listings automatically.

## Prerequisites

- Python 3.8+
- Required Python libraries (see `requirements.txt`)

To install the necessary dependencies, you can run:

```bash
pip install -r requirements.txt


Usage
Clone this repository:
bash

git clone https://github.com/mxyldrm/autoscout.git
cd autoscout-bot
Create a .env file to store your environment variables such as your Telegram API key and chat ID for error notifications:
bash

TELEGRAM_API_KEY=your_telegram_api_key
TELEGRAM_CHAT_ID=your_telegram_chat_id
Run the bot:
bash

python autoscout.py
The bot will continuously scrape new car listings and store them in the database while removing old entries.

Configuration
You can adjust the bot settings in the config.py file. This file includes key information such as:

User-Agent: Different User-Agent headers for requests.
JSON Endpoint: The bot automatically finds the JSON endpoint for the listings.
Disclaimer
This project is provided as is for educational purposes. The authors of this repository are not responsible for any issues, damages, or misuse that may arise from using this code. Use at your own risk.

The code is meant to be a learning tool for developers to explore web scraping, data extraction, and Python automation techniques.

License
This project is licensed under the MIT License. See the LICENSE file for more details.



### Key Changes:
- **English Translation:** I translated all messages to English.
- **Modular Design:** I made the code more modular with better error handling and user-friendly logging.
- **README File:** Added a professional `README.md` file with instructions, disclaimer, and setup details.

You can now publish this code on GitHub with confidence! Let me know if you need any other adjustments.
