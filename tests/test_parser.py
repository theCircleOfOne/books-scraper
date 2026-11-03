from pathlib import Path

from books_scraper.parser import parse_page, parse_price

FIXTURE = Path(__file__).parent / "fixtures" / "page-1.html"
URL = "https://books.toscrape.com/catalogue/page-1.html"


def test_parse_price_strips_symbols():
    assert parse_price("£51.77") == 51.77
    assert parse_price("Â£51.77") == 51.77


def test_parse_page_counts_and_first_book():
    books, nxt = parse_page(FIXTURE.read_text(encoding="utf-8"), URL)
    assert len(books) == 20
    first = books[0]
    assert first.title == "A Light in the Attic"
    assert first.price_gbp == 51.77
    assert first.rating == 3
    assert first.in_stock is True
    assert first.url == "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    assert nxt == "https://books.toscrape.com/catalogue/page-2.html"


def test_all_ratings_valid():
    books, _ = parse_page(FIXTURE.read_text(encoding="utf-8"), URL)
    assert all(1 <= b.rating <= 5 for b in books)
