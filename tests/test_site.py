"""Run with python3 -m unittest discover -s tests -v.

These checks catch broken visitor navigation, missing downloadable files,
and accidental exposure of telephone numbers in the page (not in the CV).
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "docs"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.resources = []
        self.text = []
        self.in_nav = False
        self.nav_links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "nav":
            self.in_nav = True
        if tag == "a":
            self.links.append(attrs)
            if self.in_nav:
                self.nav_links.append(attrs.get("href", ""))
        if tag == "img":
            self.resources.append(attrs.get("src", ""))
        if tag == "link" and attrs.get("rel") in ("stylesheet", "icon"):
            self.resources.append(attrs.get("href", ""))

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_nav = False

    def handle_data(self, data):
        self.text.append(data)


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.page = Page()
        index = ROOT / "index.html"
        if index.exists():
            self.page.feed(index.read_text(encoding="utf-8"))

    def test_visitors_can_navigate_to_real_sections(self):
        self.assertGreaterEqual(len(self.page.nav_links), 4, "Missing section navigation")
        for href in self.page.nav_links:
            self.assertTrue(href.startswith("#"), href)
            self.assertIn(href[1:], self.page.ids, "Navigation points to a missing section")
        for link in self.page.links:
            href = link.get("href", "")
            if href.startswith("#"):
                self.assertIn(href[1:], self.page.ids)

    def test_visitor_resources_resolve_inside_site(self):
        self.assertGreater(len(self.page.resources), 0, "No page resources")
        urls = self.page.resources + [link["href"] for link in self.page.links if "href" in link]
        for url in urls:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (ROOT / unquote(parsed.path).lstrip("/")).resolve()
            self.assertTrue(target.is_relative_to(ROOT.resolve()), url)
            self.assertTrue(target.is_file(), f"Missing visitor resource: {url}")

    def test_resume_link_delivers_a_pdf(self):
        downloads = [link for link in self.page.links if "download" in link]
        self.assertGreaterEqual(len(downloads), 1, "No downloadable resume")
        for link in downloads:
            target = ROOT / unquote(urlsplit(link["href"]).path).lstrip("/")
            self.assertTrue(target.is_file(), "Resume download is missing")
            self.assertEqual(target.read_bytes()[:5], b"%PDF-", "Download is not a PDF")

    def test_public_page_contacts_by_email_not_phone(self):
        contacts = [a.get("href", "") for a in self.page.links if a.get("href", "").startswith("mailto:")]
        self.assertIn("mailto:hanyangxucs@gmail.com", contacts)
        self.assertFalse(any(a.get("href", "").startswith("tel:") for a in self.page.links))
        self.assertIsNone(re.search(r"(?<!\d)1[3-9]\d{9}(?!\d)", " ".join(self.page.text)))


if __name__ == "__main__":
    unittest.main()
