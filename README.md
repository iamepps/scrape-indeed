# Scrape data-science jobs from indeed.com

This project scrapes data-science related jobs from indeed.com.

It uses selenium and headless chrome to iterate through urls scraped from indeed search pages.

The data collated in Google cloud for personal use.

The project can be run in two ways:
- Build and run in docker. This circumvents issues with chrome path and chromedriver versions, but is set up to write to Google Cloud Storage.
  - `docker build . --tag indeedscrape:latest`
  - `docker run -it -e ENV=local indeedscrape:latest`
- Run locally (write data locally rather than to Google cloud):
  - `pipenv run`

# Infra

The project runs daily in Google Cloud. The process to do this looks something like:

- The project is built in docker and stored in Google Container repository
- Cloud scheduler emits a pubsub message at 6am GMT that triggers a Cloud function to start a Google Compute VM running the docker container.
- The script runs, or errors. Either way, once it has finished it emits a pubsub message that triggers a cloud function to stop the VM.
- Logging is pushed into Google Cloud Logging.
