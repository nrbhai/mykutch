"""Batch-convert destination detail pages to use data-i18n attributes.

The script walks through every HTML file in site/destinations/, skips templates or
already-localized pages, attaches data-i18n keys to translatable elements, and
collects the English strings into the lang/*.json files under the
"destinations" namespace. Non-English language files receive the same English
text as placeholders so translators can update them later.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

from bs4 import BeautifulSoup, Tag

BASE_DIR = Path(__file__).resolve().parent
SITE_DIR = BASE_DIR / "site"
DEST_DIR = SITE_DIR / "destinations"
LANG_DIR = SITE_DIR / "lang"
LANG_CODES = ("en", "hi", "de", "fr", "es", "ru")

TRANSLATABLE_TAGS = {
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "li",
    "span",
    "small",
    "em",
    "blockquote",
    "figcaption",
    "label",
    "button",
    "th",
    "td",
    "dt",
    "dd",
    "caption",
    "summary",
}

TAG_BASE_NAMES = {
    "h1": "heading",
    "h2": "heading",
    "h3": "heading",
    "h4": "heading",
    "h5": "heading",
    "h6": "heading",
    "p": "paragraph",
    "li": "list_item",
    "span": "text_span",
    "small": "small_text",
    "em": "emphasis",
    "blockquote": "blockquote",
    "figcaption": "caption",
    "label": "label",
    "button": "button",
    "th": "table_header",
    "td": "table_cell",
    "dt": "term",
    "dd": "definition",
    "caption": "caption",
    "summary": "summary",
}

SKIP_PARENT_TAGS = {"nav", "footer", "script", "style", "noscript"}
SKIP_PARENT_IDS = {"lightbox"}


def slug_from_filename(file_path: Path) -> str:
    return file_path.stem.replace("-", "_").lower()


def has_localization_for_slug(soup: BeautifulSoup, slug_key: str) -> bool:
    def _matches(value: Optional[str]) -> bool:
        return bool(value and value.startswith(f"destinations.{slug_key}"))

    return bool(soup.find(attrs={"data-i18n": _matches}))


def is_translatable(element: Tag) -> bool:
    if element.has_attr("data-i18n"):
        return False
    if element.name not in TRANSLATABLE_TAGS:
        return False
    if element.find_parent(SKIP_PARENT_TAGS):
        return False
    if any(parent.get("id") in SKIP_PARENT_IDS for parent in element.parents if isinstance(parent, Tag)):
        return False

    text_only = element.get_text(" ", strip=True)
    if not text_only:
        return False
    if len(text_only) <= 2 and not re.search(r"[A-Za-z]", text_only):
        return False

    return True


def build_key(element: Tag, counters: Dict[str, int]) -> str:
    base = TAG_BASE_NAMES.get(element.name, element.name)
    counters[base] += 1
    return f"{base}_{counters[base]:03d}"


def element_is_within_processed(element: Tag, processed: Iterable[int]) -> bool:
    return any(id(parent) in processed for parent in element.parents if isinstance(parent, Tag))


def collect_translations(soup: BeautifulSoup, slug_key: str) -> Tuple[Dict[str, str], bool]:
    counters: Dict[str, int] = defaultdict(int)
    translations: Dict[str, str] = {}
    processed_ids = set()

    body = soup.body
    if body is None:
        return translations, False

    for element in body.descendants:
        if not isinstance(element, Tag):
            continue
        if not is_translatable(element):
            continue
        if element_is_within_processed(element, processed_ids):
            continue

        content_html = element.decode_contents().strip()
        if not content_html:
            continue

        key = build_key(element, counters)
        element["data-i18n"] = f"destinations.{slug_key}.{key}"
        translations[key] = content_html
        processed_ids.add(id(element))

    return translations, bool(translations)


def save_html(file_path: Path, soup: BeautifulSoup) -> None:
    html_output = str(soup)
    if not html_output.lstrip().lower().startswith("<!doctype"):
        html_output = "<!DOCTYPE html>\n" + html_output
    file_path.write_text(html_output, encoding="utf-8")


def update_language_files(slug_key: str, translations: Dict[str, str]) -> None:
    for lang in LANG_CODES:
        lang_path = LANG_DIR / f"{lang}.json"
        data = json.loads(lang_path.read_text(encoding="utf-8"))
        destinations_block = data.setdefault("destinations", {})
        page_block = destinations_block.setdefault(slug_key, {})

        for key, value in translations.items():
            if key in page_block:
                continue
            if lang == "en":
                page_block[key] = value
            else:
                page_block[key] = value

        lang_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def process_destination_file(file_path: Path) -> None:
    slug_key = slug_from_filename(file_path)

    html_text = file_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_text, "html.parser")

    if has_localization_for_slug(soup, slug_key):
        print(f"SKIP {file_path.name}: already has destinations.{slug_key} keys")
        return

    translations, updated = collect_translations(soup, slug_key)
    if not updated:
        print(f"SKIP {file_path.name}: no translatable content detected")
        return

    save_html(file_path, soup)
    update_language_files(slug_key, translations)
    print(f"OK   {file_path.name}: added {len(translations)} keys")


def main() -> None:
    html_files = sorted(
        f for f in DEST_DIR.glob("*.html") if not f.name.startswith("_") and f.name != "destination-slug.html"
    )

    for file_path in html_files:
        process_destination_file(file_path)


if __name__ == "__main__":
    main()
