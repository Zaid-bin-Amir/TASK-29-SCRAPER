# TASK-29-SCRAPER# Web Scraping Program

A simple Python scraper that extracts publicly available, structured information (book listings) from a website that permits scraping and saves the results to a CSV file.

## Objective

Learn the basics of:

- Making HTTP requests
- Parsing HTML
- Extracting structured data
- Saving data to CSV

## Target Website

[books.toscrape.com](https://books.toscrape.com/) is a sandbox site built specifically for scraping practice, so automated access is allowed.

## Tools Used

- Python 3
- `requests` for HTTP requests
- `BeautifulSoup` (`beautifulsoup4`) for HTML parsing
- `csv` (standard library) for writing output

## Installation

```bash
pip install requests beautifulsoup4
```

## Usage

```bash
python scraper.py
```

The script scrapes the first 5 listing pages (about 100 books) and writes the results to `books.csv` in the same folder. To scrape more pages, change `MAX_PAGES` at the top of `scraper.py`.

## How It Works

1. Checks `robots.txt` to confirm the page may be fetched.
2. Downloads the listing page with `requests`.
3. Parses the HTML with `BeautifulSoup` and reads each book card.
4. Follows the "next" link to the next page.
5. Waits 1 second between requests to keep the request rate reasonable.
6. Saves all collected rows to `books.csv`.

## Extracted Fields

| Field | Description | Source in HTML |
|---|---|---|
| `title` | Full title of the book | `title` attribute of the link inside `h3` |
| `price_gbp` | Price in British pounds (no currency symbol) | `p.price_color` |
| `rating_out_of_5` | Star rating as a number from 1 to 5 | Class name on `p.star-rating` (e.g. `Three` becomes `3`) |
| `availability` | Stock status, e.g. "In stock" | `p.availability` |
| `product_url` | Absolute link to the book's detail page | `href` of the title link |

## Output

`books.csv` with a header row and one row per book:

```
title,price_gbp,rating_out_of_5,availability,product_url
```

## Responsible Scraping

- Only scrape websites where automated access is permitted.
- Respect `robots.txt` and the website's terms of use.
- Use reasonable request rates (this script waits 1 second between pages).
- Identify your scraper with a clear User-Agent.

## Project Files

- `scraper.py` : the web scraper
- `books.csv` : the extracted dataset (created after running the scraper)
- `README.md` : this file
