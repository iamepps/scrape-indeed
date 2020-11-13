import json
import logging
import random
import re
from requests.models import PreparedRequest
from src.driver import initialise_driver
from time import sleep

logging.getLogger(__name__)

def inject_params(url, params):
    req = PreparedRequest()
    req.prepare_url(url, params)
    return req.url


def get_n_results(driver, config, params):
    url = inject_params(config["serp_base_url"], params)
    driver.get(url)
    raw_count_text = driver.find_element_by_id("searchCount").text
    count_raw = raw_count_text.split("of")[-1]
    count_clean = re.findall("[0-9]", count_raw)
    return int("".join(count_clean))


def n_pages_to_scrape(n_results, config):
    if config.get("serps_limit"):
        return config.get("serps_limit")
    else:
        return 1 + n_results // config["results_per_page"]


def load_seen_vacancies():
    None


def parse_cards(driver):
    def parse_job_card(card):
        card_title = card.find_element_by_class_name("title")
        card_data = {
            "title": card_title.text,
            "url": card_title.find_element_by_tag_name("a").get_attribute("href"),
            "company": card.find_element_by_class_name("company").text,
        }
        return card_data

    job_cards = driver.find_elements_by_css_selector(".clickcard")

    base_data = []

    for card in job_cards:
        base_data.append(parse_job_card(card))

    return base_data


def scrape_serps(driver, config, params, n_to_scrape):

    job_stubs = []

    for i in range(n_to_scrape):
        params["start"] = i
        url = inject_params(config["serp_base_url"], params)
        driver.get(url)
        job_stubs.extend(parse_cards(driver))

    return job_stubs


def scrape_jdp(driver, url):
    driver.get(url)
    header_text = driver.find_element_by_css_selector(
        ".jobsearch-DesktopStickyContainer"
    ).text
    ad_text = driver.find_element_by_id("jobDescriptionText").text
    sleep(int(abs(random.gauss(5, 2))))  # basic attempt to avoid captcha!
    return header_text, ad_text


def shuffle(l):
    return sorted(l, key=lambda x: random.random())


def scrape(params, config, bucket, TODAY):

    driver = initialise_driver()

    n_results = get_n_results(driver, config, params)
    logging.info(f"{n_results} results in {params['l']}")

    n_serps_to_scrape = n_pages_to_scrape(n_results, config)

    try:
        live_jobs = scrape_serps(driver, config, params, n_serps_to_scrape)
        distinct_urls = {job['url'] for job in live_jobs}
        logging.info(f"Collected {len(live_jobs)} jobs ({len(distinct_urls)} distinct urls) from search pages.")
    except Exception as e:
        raise e
        logging.error("Failed to scrape SERPs")


    scraped_urls = json.loads(bucket.read("indeed/scraped_urls.json"))
    logging.info(f"Loaded {len(scraped_urls)} previously scraped jobs")

    new_jobs = [job for job in live_jobs if job["url"] not in scraped_urls]
    logging.info(f"Found {len(new_jobs)} unseen jobs to scrape")

    scraped_jobs = []

    try:
        jobs_to_scrape = shuffle(new_jobs[: config.get("jobs_per_serp_limit")])
        for i, job in enumerate(jobs_to_scrape):

            if i % 50 == 0:
                logging.info(f"scraping url {i}")

            header_text, ad_text = scrape_jdp(driver, job["url"])
            job["header_text"] = header_text
            job["ad_text"] = ad_text
            scraped_jobs.append(job)
            scraped_urls.append(job["url"])

    except Exception as e:
        logging.error(e)
        logging.error(f"Failed to scrape {job['url']}")

    finally:
        # update scraped url history
        bucket.write("indeed/scraped_urls_tmp.json", json.dumps(list(scraped_urls)))
        bucket.rewrite("indeed/scraped_urls.json", "indeed/scraped_urls_tmp.json")
        bucket.delete("indeed/scraped_urls_tmp.json")


        # write daily output
        output_path = f"indeed/daily/{params['l']}-{'-'.join(params['q'].split(' '))}-{TODAY}.json"
        if len(bucket.list_keys(output_path)) > 0:
            bucket.append(output_path, scraped_jobs)
        else:
            bucket.write(output_path, json.dumps(scraped_jobs))
        driver.quit()

    return len(scraped_urls)
