# books-scraper

Small, tested web scraper: crawls a paginated catalogue and exports clean **CSV** and **Excel (.xlsx)**.
Demo target is [books.toscrape.com](https://books.toscrape.com), a sandbox site built for scraping practice.

## What it shows
- Pagination crawling with a request delay and retry/backoff (polite to the server)
- Parsing separated from networking, so it is unit-tested offline against a saved HTML fixture
- Clean output: typed fields (price as number, rating 1-5, stock as boolean), Excel with frozen header, filters and auto-width columns; CSV opens correctly in Excel (UTF-8 with BOM)

## Usage (PowerShell)
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m books_scraper --pages 5 --out output
pytest
```
Options: `--pages` (1-50, 20 books per page), `--delay` seconds between requests, `--out` directory.

## Sample output
See [`examples/books.csv`](examples/books.csv) and [`examples/books.xlsx`](examples/books.xlsx) (60 books, 3 pages).

| title | price_gbp | rating | in_stock | url |
|---|---|---|---|---|
| A Light in the Attic | 51.77 | 3 | True | https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html |
| Tipping the Velvet | 53.74 | 1 | True | https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html |

## Adapting to your site
Selectors live in one place (`books_scraper/parser.py`); the crawler and exporters are generic.
Custom scrapers (other sites, login, JS-rendered pages, scheduled runs, Telegram/Google Sheets delivery) are available on request.

## Structure
```
books_scraper/   parser.py (HTML -> objects), scraper.py (crawl), export.py (CSV/XLSX), __main__.py (CLI)
tests/           offline tests + saved HTML fixture
examples/        sample CSV/XLSX
```
