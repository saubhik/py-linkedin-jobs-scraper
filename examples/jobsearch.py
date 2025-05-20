from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import (
    RelevanceFilters,
    TimeFilters,
    TypeFilters,
    ExperienceLevelFilters,
    IndustryFilters,
)
import telegram_send
import time
import asyncio
import re

seen = set()


def on_data(data: EventData):
    contains_keywords = any(
        keyword in data.description.casefold()
        for keyword in [
            "selenium",
            "java",
            "c#",
            ".net",
            "python",
            "javascript",
            "c++",
            "cpp",
            "sql",
            "azure",
            "tableau",
            "QA",
            "cypress",
            "playwright",
        ]
    )
    if not contains_keywords:
        return

    # if data in seen:
    #     return

    # seen.add(data)

    # Get the job ID.
    match = re.search(r"/(\d+)/", data.link)
    if not match:
        match = re.search(r"currentJobId=(\d+)", data.link)
    job_id = match.group(1)
    url = f"https://www.linkedin.com/jobs/view/{job_id}/"

    asyncio.run(
        telegram_send.send(
            messages=[
                f"Title: {data.title}\nCompany: {data.company}\nDate: {data.date}\nLink: {url}"
            ]
        )
    )
    print(
        "[ON_DATA]",
        data.title,
        data.company,
        data.date,
        url,
        len(data.description),
    )


def on_error(error):
    print("[ON_ERROR]", error)


def on_end():
    print("[ON_END]")


scraper = LinkedinScraper(
    chrome_options=None,  # You can pass your custom Chrome options here
    max_workers=3,  # How many threads will be spawn to run queries concurrently (one Chrome driver for each thread)
    slow_mo=0.5,  # Slow down the scraper to avoid 'Too many requests (429)' errors
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    Query(
        options=QueryOptions(
            locations=["Toronto", "Greater Toronto Area", "Ontario"],
            limit=500,
            apply_link=True,
            skip_promoted_jobs=True,
            filters=QueryFilters(
                company_jobs_url=None,
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.DAY,
                type=None,
                experience=[
                    ExperienceLevelFilters.ENTRY_LEVEL,
                    ExperienceLevelFilters.ASSOCIATE,
                    ExperienceLevelFilters.MID_SENIOR,
                ],
                on_site_or_remote=None,
                industry=None,
            ),
        ),
    )
]

while True:
    scraper.run(queries)
    if len(seen) > 100_000:
        seen.clear()
