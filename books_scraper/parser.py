"""HTML parsing for books.toscrape.com catalogue pages (pure, no network)."""
from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


@dataclass(frozen=True)
class Book:
    title: str
    price_gbp: float
    rating: int  # 1..5
    in_stock: bool
    url: str
    image_url: str


def parse_price(text: str) -> float:
    """'£51.77' -> 51.77 (GBP). Strips any currency symbol / mojibake."""
    cleaned = "".join(ch for ch in text if ch.isdigit() or ch == ".")
    return float(cleaned)


def parse_page(html: str, page_url: str) -> tuple[list[Book], str | None]:
    """Return (books, next_page_url or None) for one catalogue page."""
    soup = BeautifulSoup(html, "html.parser")
    books: list[Book] = []
    for card in soup.select("article.product_pod"):
        link = card.select_one("h3 a")
        rating_cls = card.select_one("p.star-rating")["class"]
        rating = next((RATING_WORDS[c] for c in rating_cls if c in RATING_WORDS), 0)
        books.append(
            Book(
                title=link["title"],
                price_gbp=parse_price(card.select_one("p.price_color").get_text()),
                rating=rating,
                in_stock="in stock" in card.select_one("p.availability").get_text().lower(),
                url=urljoin(page_url, link["href"]),
                image_url=urljoin(page_url, card.select_one("img")["src"]),
            )
        )
    nxt = soup.select_one("li.next a")
    return books, (urljoin(page_url, nxt["href"]) if nxt else None)
