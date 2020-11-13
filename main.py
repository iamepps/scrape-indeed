import datetime
import google.cloud.logging
import os
import logging
from src.mop_up import server_down
from src.config import load_config
from src.gcs import Gcs
from src.scrape import scrape


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

        locations = config.get("locations")

        for location in locations:

            params = {
                "q": "data scientist",
                "l": location,
                "limit": config["results_per_page"],
                "start": 0,
            }

            logging.info(f"Finding jobs in {location}")

            n_results = scrape(params, config, bucket, TODAY)

    except Exception as e:
        raise e
        logging.error(e)

    finally:

        server_down(config)

if __name__ == "__main__":
    main()
