import requests
import random
from datetime import datetime
from common import logger, send_error_to_telegram, insert_car_to_database, delete_old_cars_from_database
from playwright.sync_api import sync_playwright
import time

bot_name = "AutoScout Bot"

# List of different User-Agent headers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

# Function to find JSON endpoint
def find_json_endpoint():
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            json_endpoint = None

            # Function to be called when a network request is made
            def handle_response(response):
                nonlocal json_endpoint
                if 'lst.json' in response.url:
                    json_endpoint = response.url

            page.on("response", handle_response)

            # Open the page
            try:
                page.goto("https://www.autoscout24.de/lst?atype=C&cy=D&damaged_listing=exclude&desc=0&ocs_listing=include&powertype=kw&search_id=26fztiow6l9&sort=leasing_rate&source=homepage_search-mask&ustate=N%2CU", timeout=60000)
            except Exception as e:
                error_message = f"{bot_name} - Page loading error: {str(e)}"
                logger.error(error_message)
                send_error_to_telegram(error_message)
                return None

            # Make dropdown selection and wait for the page to fully load
            try:
                page.select_option("#sort-dropdown-select", "age-descending")
                page.wait_for_load_state("networkidle", timeout=60000)
            except Exception as e:
                error_message = f"{bot_name} - Dropdown selection or network idle wait error: {str(e)}"
                logger.error(error_message)
                send_error_to_telegram(error_message)
                return None

            browser.close()

            if json_endpoint is None:
                error_message = f"{bot_name} - JSON endpoint not found. Please check the page and network requests."
                logger.error(error_message)
                send_error_to_telegram(error_message)

            return json_endpoint
    except Exception as e:
        error_message = f"{bot_name} - General error: {str(e)}"
        logger.error(error_message)
        send_error_to_telegram(error_message)
        return None

# Function to check for new listings
def check_new_listings(json_url):
    try:
        for page_num in [1, 2]:
            paged_url = json_url.replace("page=1", f"page={page_num}")
            headers = {
                "User-Agent": random.choice(user_agents)
            }

            response = requests.get(paged_url, headers=headers)
            response.raise_for_status()
            json_data = response.json()

            listings = json_data['pageProps']['listings']
            new_car_count = 0

            for listing in listings:
                car_id = listing['id']
                make = listing['vehicle'].get('make', 'Unknown make')
                model = listing['vehicle'].get('model', 'Unknown model')
                model_version = listing['vehicle'].get('modelVersionInput', '')
                model_and_brand = f"{make} {model} {model_version}".strip()

                price_text = listing.get('price', {}).get('priceFormatted', 'Unknown price')
                images = listing.get('images', [])
                img_src = images[0] if images else 'Image not available'

                car_link = "https://www.autoscout24.de" + listing.get('url', '')

                vehicle_details = listing.get('vehicleDetails', [])
                features = {}
                for detail in vehicle_details:
                    icon_name = detail.get('iconName')
                    data = detail.get('data', 'Unknown')
                    if icon_name:
                        features[icon_name] = data

                car_info = {
                    'ID': car_id,
                    'Image': img_src,
                    'Model and Make': model_and_brand,
                    'Link': car_link,
                    'Price': price_text,
                    'Company': 'autoscout24',
                    'Features': features,
                    'Transmission': features.get('transmission', 'Unknown')
                }

                insert_car_to_database(car_info, bot_name)
                new_car_count += 1

    except requests.RequestException as e:
        error_message = f"{bot_name} - Error during request: {e}"
        logger.error(error_message)
        send_error_to_telegram(error_message)
    except Exception as e:
        error_message = f"{bot_name} - Unexpected error: {e}"
        logger.error(error_message)
        send_error_to_telegram(error_message)

# Main function
def main():
    while True:
        try:
            logger.info(f"{bot_name} - Main loop started.")
            json_endpoint = find_json_endpoint()
            if json_endpoint:
                check_new_listings(json_endpoint)
            else:
                error_message = f"{bot_name} - JSON endpoint not found and could not proceed."
                logger.error(error_message)
                send_error_to_telegram(error_message)

            delete_old_cars_from_database()
        except Exception as e:
            error_message = f"{bot_name} - Unexpected error during infinite loop: {e}"
            logger.error(error_message)
            send_error_to_telegram(error_message)

        time.sleep(60)  # Wait 1 minute
