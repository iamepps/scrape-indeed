import datetime
import google.cloud.logging
import os
import json
import logging
import random
from src.config import load_config
from src.gcs import Gcs
from src.scrape import scrape
from selenium.webdriver.common.keys import Keys
from time import sleep

if not os.getenv("ENV"):
    os.environ["ENV"] = "local"

if os.getenv("ENV") == "local":
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"
    ] = "./config/secrets/scrapes-276809-909508a2a0c4.json"
else:
    client = google.cloud.logging.Client()
    client.get_default_handler()
    client.setup_logging()



TODAY = datetime.datetime.now().strftime("%Y-%m-%d")

bucket = Gcs(bucket="ame-scrapes")

config = load_config(secrets_path="config/secrets/secrets.json")

logging.basicConfig(filename="log.log", level=logging.INFO)


def main():
    try:
        bucket.write('test.json', json.dumps(["this", "is", "a", "test"]))

        locations = config.get("locations")

        for location in locations:

            params = {
                "q": "data scientist",
                "l": location,
                "limit": config["results_per_page"],
                "start": 0,
            }

            logging.info(f"Scraping {params['q']} jobs in {params['l']}")

            logging.info(f"Finding jobs in {location}")
            n_results = scrape(params, config, bucket, TODAY)

    except Exception as e:
        raise e
        logging.error(e)


if __name__ == "__main__":
    main()
