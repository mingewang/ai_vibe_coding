import time
import re
from typing import List
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from src.config import config


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    return clean_text(text)


def is_same_domain(url: str, base_domain: str) -> bool:
    parsed = urlparse(url)
    return base_domain in parsed.netloc


def crawl_site(
    start_url: str,
    max_pages: int = None,
    max_depth: int = None,
    delay: float = None,
) -> List[dict]:
    if max_pages is None:
        max_pages = config.crawler_max_pages
    if max_depth is None:
        max_depth = config.crawler_max_depth
    if delay is None:
        delay = config.crawler_delay

    base_domain = urlparse(start_url).netloc
    visited = set()
    to_visit = [(start_url, 0)]
    pages = []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    while to_visit and len(pages) < max_pages:
        url, depth = to_visit.pop(0)

        if url in visited or depth > max_depth:
            continue
        visited.add(url)

        try:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [skip] {url} — {e}")
            continue

        text = extract_text_from_html(resp.text)
        if len(text) < 50:
            continue

        pages.append({"url": url, "text": text, "depth": depth})
        print(f"  [{len(pages)}] depth={depth} {url} ({len(text)} chars)")

        if depth < max_depth:
            soup = BeautifulSoup(resp.text, "lxml")
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                full_url = urljoin(url, href)
                parsed = urlparse(full_url)
                if parsed.scheme in ("http", "https") and is_same_domain(
                    full_url, base_domain
                ):
                    clean = parsed._replace(fragment="").geturl()
                    if clean not in visited:
                        to_visit.append((clean, depth + 1))

        time.sleep(delay)

    return pages
