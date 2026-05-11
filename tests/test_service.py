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

    # --- expiration edge cases ---

    def test_create_link_rejects_non_iso_expiration(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.create_link("https://example.com", "not-a-date")

    def test_create_link_naive_datetime_treated_as_utc(self) -> None:
        expires_at = (utc_now() + timedelta(hours=1)).replace(tzinfo=None).isoformat()
        link = self.service.create_link("https://example.com", expires_at)
        self.assertIsNotNone(link.expires_at)

    def test_expired_link_shows_expired_flag_in_list(self) -> None:
        link = self.service.create_link(
            "https://example.com", (utc_now() + timedelta(seconds=1)).isoformat()
        )
        repo_links = self.service.repository.list_links()
        for item in repo_links:
            if item.code == link.code:
                item.expires_at = (utc_now() - timedelta(seconds=1)).isoformat()
        self.service.repository.save_links(repo_links)
        items = self.service.list_links()
        expired_item = next(i for i in items if i["code"] == link.code)
        self.assertTrue(expired_item["expired"])

    def test_no_expiration_link_never_expires(self) -> None:
        link = self.service.create_link("https://example.com")
        item = self.service.get_link(link.code)
        self.assertIsNone(item["expires_at"])
        self.assertFalse(item["expired"])

    # --- click counter edge cases ---

    def test_multiple_resolves_increment_clicks_each_time(self) -> None:
        link = self.service.create_link("https://example.com")
        self.service.resolve_link(link.code)
        self.service.resolve_link(link.code)
        self.service.resolve_link(link.code)
        item = self.service.get_link(link.code)
        self.assertEqual(item["clicks"], 3)

    def test_expired_link_resolve_does_not_increment_clicks(self) -> None:
        link = self.service.create_link(
            "https://example.com", (utc_now() + timedelta(seconds=1)).isoformat()
        )
        repo_links = self.service.repository.list_links()
        for item in repo_links:
            if item.code == link.code:
                item.expires_at = (utc_now() - timedelta(seconds=1)).isoformat()
        self.service.repository.save_links(repo_links)
        with self.assertRaises(ExpiredLinkError):
            self.service.resolve_link(link.code)
        item = self.service.get_link(link.code)
        self.assertEqual(item["clicks"], 0)

    def test_clicks_persist_across_repository_reloads(self) -> None:
        link = self.service.create_link("https://example.com")
        self.service.resolve_link(link.code)
        repo2 = JsonLinkRepository(self.service.repository.file_path)
        service2 = ShortLinkService(repo2)
        item = service2.get_link(link.code)
        self.assertEqual(item["clicks"], 1)


if __name__ == "__main__":
    unittest.main()
