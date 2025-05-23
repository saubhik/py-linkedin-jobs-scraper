from enum import Enum
from typing import NamedTuple
from typing import List


class Events(Enum):
    DATA = "scraper:data"
    METRICS = "scraper:metrics"
    END = "scraper:end"
    ERROR = "scraper:error"
    INVALID_SESSION = "scraper:invalid-session"


class EventData(NamedTuple):
    query: str = ""
    location: str = ""
    job_id: str = ""
    job_index: int = -1  # Only for debug
    link: str = ""
    apply_link: str = ""
    title: str = ""
    company: str = ""
    company_link: str = ""
    company_img_link: str = ""
    place: str = ""
    description: str = ""
    description_html: str = ""
    date: str = ""
    date_text: str = ""
    insights: List[str] = []
    skills: List[str] = []

    def __hash__(self):
        return (
            hash(self.title)
            ^ hash(self.company)
            ^ hash(self.date)
            ^ hash(self.description)
        )

    def __eq__(self, other):
        return (
            self.title == other.title
            and self.company == other.company
            and self.date == other.date
            and self.description == other.description
        )


class EventMetrics:
    processed: int = 0  # Number of successfully processed jobs
    failed: int = 0  # Number of jobs failed to process
    missed: int = 0  # Number of missed jobs to load during scraping
    skipped: int = 0  # Number of skipped jobs

    def __str__(self):
        return f"{{ processed: {self.processed}, failed: {self.failed}, missed: {self.missed}, skipped: {self.skipped} }}"
