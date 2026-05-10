from __future__ import annotations

import secrets
import string
from dataclasses import asdict
from datetime import datetime, timezone
from urllib.parse import urlparse

from .models import Link, utc_now
from .repository import JsonLinkRepository


class LinkNotFoundError(KeyError):
    pass


class ExpiredLinkError(ValueError):
    pass


class ValidationError(ValueError):
    pass


class ShortLinkService:
    def __init__(self, repository: JsonLinkRepository) -> None:
        self.repository = repository

    def create_link(self, target_url: str, expires_at: str | None = None) -> Link:
        self._validate_url(target_url)
        parsed_expiry = self._parse_expiration(expires_at) if expires_at else None
        links = self.repository.list_links()
        code = self._generate_unique_code({link.code for link in links})
        link = Link(
            code=code,
            target_url=target_url,
            created_at=utc_now().isoformat(),
            expires_at=parsed_expiry.isoformat() if parsed_expiry else None,
            clicks=0,
        )
        links.append(link)
        self.repository.save_links(links)
        return link

    def list_links(self, status: str = "all") -> list[dict[str, object]]:
        now = utc_now()
        links = self.repository.list_links()
        items = [self._to_view(link, now) for link in links]
        if status == "active":
            items = [item for item in items if not item["expired"]]
        elif status == "expired":
            items = [item for item in items if item["expired"]]
        return sorted(items, key=lambda item: item["created_at"], reverse=True)

    def resolve_link(self, code: str) -> str:
        links = self.repository.list_links()
        now = utc_now()
        for link in links:
            if link.code != code:
                continue
            if link.is_expired(now):
                raise ExpiredLinkError(f"Link '{code}' has expired")
            link.clicks += 1
            self.repository.save_links(links)
            return link.target_url
        raise LinkNotFoundError(code)

    def delete_link(self, code: str) -> None:
        links = self.repository.list_links()
        remaining = [link for link in links if link.code != code]
        if len(remaining) == len(links):
            raise LinkNotFoundError(code)
        self.repository.save_links(remaining)

    def get_link(self, code: str) -> dict[str, object]:
        now = utc_now()
        for link in self.repository.list_links():
            if link.code == code:
                return self._to_view(link, now)
        raise LinkNotFoundError(code)

    def _to_view(self, link: Link, now: datetime) -> dict[str, object]:
        data = asdict(link)
        data["expired"] = link.is_expired(now)
        return data

    def _generate_unique_code(self, existing_codes: set[str], length: int = 6) -> str:
        alphabet = string.ascii_letters + string.digits
        while True:
            code = "".join(secrets.choice(alphabet) for _ in range(length))
            if code not in existing_codes:
                return code

    def _validate_url(self, target_url: str) -> None:
        parsed = urlparse(target_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValidationError("URL must use http or https and include a host")

    def _parse_expiration(self, expires_at: str) -> datetime:
        try:
            parsed = datetime.fromisoformat(expires_at)
        except ValueError as exc:
            raise ValidationError("Expiration must be a valid ISO-8601 datetime") from exc
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        if parsed <= utc_now():
            raise ValidationError("Expiration must be in the future")
        return parsed
