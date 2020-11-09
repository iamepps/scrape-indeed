# Scrape indeed.com

This project scrapes data-science and related jobs from indeed.com.

It uses selenium and headless chrome.

The data collated in Google cloud for personal use. 

The project can be run in a number of ways:
- `pipenv run python main.py` to run the project locally.
- Build and run in docker:
  - `docker build . --tag indeedscrape:latest`
  - `docker run -it -e ENV=local indeedscrape:latest`
