from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Link:
    code: str
    target_url: str
    created_at: str
    expires_at: str | None
    clicks: int = 0

    def is_expired(self, now: datetime | None = None) -> bool:
        if not self.expires_at:
            return False
        check_time = now or utc_now()
        return datetime.fromisoformat(self.expires_at) <= check_time

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "Link":
        return cls(
            code=str(payload["code"]),
            target_url=str(payload["target_url"]),
            created_at=str(payload["created_at"]),
            expires_at=str(payload["expires_at"]) if payload.get("expires_at") else None,
            clicks=int(payload.get("clicks", 0)),
        )
