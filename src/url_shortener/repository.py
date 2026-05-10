from __future__ import annotations

import json
from pathlib import Path

from .models import Link


class JsonLinkRepository:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def list_links(self) -> list[Link]:
        payload = json.loads(self.file_path.read_text(encoding="utf-8"))
        return [Link.from_dict(item) for item in payload]

    def save_links(self, links: list[Link]) -> None:
        serialized = [link.to_dict() for link in links]
        self.file_path.write_text(
            json.dumps(serialized, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
