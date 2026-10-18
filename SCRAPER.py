"""Simple web scraper: extracts book data from books.toscrape.com into a CSV.

books.toscrape.com is a sandbox site built for scraping practice, so automated
access is explicitly allowed. The script still checks robots.txt and waits
between requests to stay polite.
"""

import csv
import time
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
START_URL = urljoin(BASE_URL, "catalogue/page-1.html")
OUTPUT_FILE = "books.csv"
MAX_PAGES = 5          # keep the crawl small
DELAY_SECONDS = 1.0    # reasonable request rate
USER_AGENT = "LearningScraper/1.0 (educational project)"

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def allowed_by_robots(url):
    """Return True if robots.txt permits fetching this URL."""
    parser = RobotFileParser()
    parser.set_url(urljoin(BASE_URL, "robots.txt"))
    try:
        parser.read()
    except Exception:
        return True  # no readable robots.txt -> no restrictions published
    return parser.can_fetch(USER_AGENT, url)


def fetch(session, url):
    response = session.get(url, timeout=15)
    response.raise_for_status()
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "html.parser")


def parse_books(soup, page_url):
    """Extract one dict per book card on a listing page."""
    books = []
    for card in soup.select("article.product_pod"):
        link = card.h3.a
        rating_class = card.select_one("p.star-rating")["class"]
        rating = next((RATING_WORDS[c] for c in rating_class if c in RATING_WORDS), None)
        books.append({
            "title": link["title"],
            "price_gbp": card.select_one("p.price_color").get_text(strip=True).lstrip("£Â"),
            "rating_out_of_5": rating,
            "availability": card.select_one("p.availability").get_text(strip=True),
            "product_url": urljoin(page_url, link["href"]),
        })
    return books


def main():
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    all_books = []
    url = START_URL
    for _ in range(MAX_PAGES):
        if not allowed_by_robots(url):
            print(f"Blocked by robots.txt: {url}")
            break
        print(f"Scraping {url}")
        soup = fetch(session, url)
        all_books.extend(parse_books(soup, url))

        next_link = soup.select_one("li.next a")
        if not next_link:
            break
        url = urljoin(url, next_link["href"])
        time.sleep(DELAY_SECONDS)

    fields = ["title", "price_gbp", "rating_out_of_5", "availability", "product_url"]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_books)

    print(f"Saved {len(all_books)} books to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()