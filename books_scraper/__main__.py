"""CLI: python -m books_scraper --pages 5 --out output"""
from __future__ import annotations

import argparse
from pathlib import Path

from .export import to_csv, to_xlsx
from .scraper import crawl


def main() -> None:
    ap = argparse.ArgumentParser(description="Scrape books.toscrape.com into CSV/XLSX")
    ap.add_argument("--pages", type=int, default=3, help="number of catalogue pages (20 books each, max 50)")
    ap.add_argument("--delay", type=float, default=0.5, help="seconds between requests")
    ap.add_argument("--out", type=Path, default=Path("output"), help="output directory")
    args = ap.parse_args()

    books = list(crawl(max_pages=args.pages, delay=args.delay))
    args.out.mkdir(parents=True, exist_ok=True)
    to_csv(books, args.out / "books.csv")
    to_xlsx(books, args.out / "books.xlsx")
    print(f"Saved {len(books)} books to {args.out.resolve()}")


if __name__ == "__main__":
    main()
