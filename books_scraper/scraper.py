"""Polite crawler: follows pagination with a delay and retries."""
from __future__ import annotations

import time
from collections.abc import Iterator

import requests

from .parser import Book, parse_page

START_URL = "https://books.toscrape.com/catalogue/page-1.html"
USER_AGENT = "books-scraper-demo/1.0 (portfolio project)"


def fetch(session: requests.Session, url: str, retries: int = 3, timeout: float = 20.0) -> str:
    """GET with simple exponential backoff on network / 5xx errors."""
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=timeout)
            if r.status_code >= 500:
                raise requests.HTTPError(f"{r.status_code} for {url}")
            r.raise_for_status()
            r.encoding = "utf-8"
            return r.text
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(2**attempt)
    raise AssertionError("unreachable")


def crawl(max_pages: int = 3, delay: float = 0.5, start_url: str = START_URL) -> Iterator[Book]:
    """Yield books from up to `max_pages` pages (delay seconds between requests)."""
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    url: str | None = start_url
    for _ in range(max_pages):
        if url is None:
            break
        books, url = parse_page(fetch(session, url), url)
        yield from books
        if url is not None:
            time.sleep(delay)
