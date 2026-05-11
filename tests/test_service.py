from __future__ import annotations

import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from src.url_shortener.models import utc_now
from src.url_shortener.repository import JsonLinkRepository
from src.url_shortener.service import ExpiredLinkError, LinkNotFoundError, ShortLinkService, ValidationError


class ShortLinkServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        repo = JsonLinkRepository(Path(self.temp_dir.name) / "links.json")
        self.service = ShortLinkService(repo)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_create_link_generates_code(self) -> None:
        link = self.service.create_link("https://example.com")
        self.assertEqual(len(link.code), 6)

    def test_create_link_sets_clicks_to_zero(self) -> None:
        link = self.service.create_link("https://example.com")
        self.assertEqual(link.clicks, 0)

    def test_create_link_rejects_invalid_scheme(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.create_link("ftp://example.com/file")

    def test_create_link_rejects_missing_host(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.create_link("https:///missing-host")

    def test_create_link_accepts_future_expiration(self) -> None:
        expires_at = (utc_now() + timedelta(hours=2)).isoformat()
        link = self.service.create_link("https://example.com", expires_at)
        self.assertEqual(link.expires_at, expires_at)

    def test_create_link_rejects_past_expiration(self) -> None:
        expires_at = (utc_now() - timedelta(minutes=1)).isoformat()
        with self.assertRaises(ValidationError):
            self.service.create_link("https://example.com", expires_at)

    def test_list_links_returns_items(self) -> None:
        self.service.create_link("https://example.com/1")
        self.service.create_link("https://example.com/2")
        self.assertEqual(len(self.service.list_links()), 2)

    def test_active_filter_excludes_expired_links(self) -> None:
        self.service.create_link("https://example.com/active")
        expired = self.service.create_link("https://example.com/expired", (utc_now() + timedelta(seconds=1)).isoformat())
        repo_links = self.service.repository.list_links()
        for link in repo_links:
            if link.code == expired.code:
                link.expires_at = (utc_now() - timedelta(seconds=1)).isoformat()
        self.service.repository.save_links(repo_links)
        items = self.service.list_links("active")
        self.assertEqual(len(items), 1)

    def test_expired_filter_includes_only_expired_links(self) -> None:
        self.service.create_link("https://example.com/active")
        expiring = self.service.create_link("https://example.com/expired", (utc_now() + timedelta(seconds=1)).isoformat())
        repo_links = self.service.repository.list_links()
        for link in repo_links:
            if link.code == expiring.code:
                link.expires_at = (utc_now() - timedelta(seconds=1)).isoformat()
        self.service.repository.save_links(repo_links)
        items = self.service.list_links("expired")
        self.assertEqual(len(items), 1)
        self.assertTrue(items[0]["expired"])

    def test_resolve_link_increments_clicks(self) -> None:
        link = self.service.create_link("https://example.com")
        target = self.service.resolve_link(link.code)
        self.assertEqual(target, "https://example.com")
        saved = self.service.get_link(link.code)
        self.assertEqual(saved["clicks"], 1)

    def test_resolve_link_raises_for_missing_code(self) -> None:
        with self.assertRaises(LinkNotFoundError):
            self.service.resolve_link("missing")

    def test_resolve_link_raises_for_expired_code(self) -> None:
        link = self.service.create_link("https://example.com", (utc_now() + timedelta(seconds=1)).isoformat())
        repo_links = self.service.repository.list_links()
        for item in repo_links:
            if item.code == link.code:
                item.expires_at = (utc_now() - timedelta(seconds=1)).isoformat()
        self.service.repository.save_links(repo_links)
        with self.assertRaises(ExpiredLinkError):
            self.service.resolve_link(link.code)

    def test_delete_link_removes_link(self) -> None:
        link = self.service.create_link("https://example.com")
        self.service.delete_link(link.code)
        self.assertEqual(self.service.list_links(), [])

    def test_delete_link_raises_for_missing_code(self) -> None:
        with self.assertRaises(LinkNotFoundError):
            self.service.delete_link("missing")

    def test_get_link_returns_expired_flag(self) -> None:
        link = self.service.create_link("https://example.com")
        item = self.service.get_link(link.code)
        self.assertFalse(item["expired"])


if __name__ == "__main__":
    unittest.main()
