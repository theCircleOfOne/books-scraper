"""CSV / XLSX export."""
from __future__ import annotations

import csv
from dataclasses import asdict, fields
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

from .parser import Book

COLUMNS = [f.name for f in fields(Book)]


def to_csv(books: list[Book], path: Path) -> None:
    # utf-8-sig so Excel opens non-ASCII titles correctly
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(asdict(b) for b in books)


def to_xlsx(books: list[Book], path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "books"
    ws.append(COLUMNS)
    for c in ws[1]:
        c.font = Font(bold=True)
    for b in books:
        ws.append([getattr(b, col) for col in COLUMNS])
    for i, col in enumerate(COLUMNS, start=1):
        width = max(len(col), *(len(str(getattr(b, col))) for b in books)) if books else len(col)
        ws.column_dimensions[get_column_letter(i)].width = min(width + 2, 60)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    wb.save(path)
