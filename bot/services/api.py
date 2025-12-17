from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import aiohttp


@dataclass(frozen=True)
class BackendConfig:
    base_url: str
    bot_secret: str


class BackendAPI:
    def __init__(self, cfg: BackendConfig) -> None:
        self._cfg = cfg

    def _headers(self, telegram_id: int) -> dict[str, str]:
        return {
            "X-Bot-Secret": self._cfg.bot_secret,
            "X-Telegram-Id": str(telegram_id),
            "Content-Type": "application/json",
        }

    async def list_tasks(self, telegram_id: int) -> list[dict[str, Any]]:
        url = f"{self._cfg.base_url}/api/tasks/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers(telegram_id)) as resp:
                data = await resp.json(content_type=None)
                if resp.status >= 400:
                    raise RuntimeError(f"Ошибка в бэкенде {resp.status}: {data}")
                return data


    async def list_categories(self, telegram_id: int) -> list[dict[str, Any]]:
        url = f"{self._cfg.base_url}/api/categories/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers(telegram_id)) as resp:
                data = await resp.json(content_type=None)
                if resp.status >= 400:
                    raise RuntimeError(f"Ошибка в бэкенде {resp.status}: {data}")
                return data

    async def create_category(self, telegram_id: int, name: str) -> dict[str, Any]:
        url = f"{self._cfg.base_url}/api/categories/"
        payload = {"name": name}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self._headers(telegram_id), json=payload) as resp:
                data = await resp.json(content_type=None)
                if resp.status >= 400:
                    raise RuntimeError(f"Ошибка в бэкенде {resp.status}: {data}")
                return data

    async def get_or_create_category_by_name(self, telegram_id: int, name: str) -> dict[str, Any]:
        name_norm = name.strip()
        if not name_norm:
            raise ValueError("Пустое имя категории")

        categories = await self.list_categories(telegram_id)
        for c in categories:
            if (c.get("name") or "").strip().lower() == name_norm.lower():
                return c

        return await self.create_category(telegram_id, name_norm)

    async def create_task(
            self,
            telegram_id: int,
            title: str,
            description: str = "",
            category_ids: list[str] | None = None,
            due_at: str | None = None,
    ) -> dict[str, Any]:

        url = f"{self._cfg.base_url}/api/tasks/"
        payload: dict[str, Any] = {"title": title, "description": description}

        if due_at:
            payload["due_at"] = due_at

        if category_ids is not None:
            payload["categories"] = category_ids

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self._headers(telegram_id), json=payload) as resp:
                data = await resp.json(content_type=None)
                if resp.status >= 400:
                    raise RuntimeError(f"Ошибка в бэкенде {resp.status}: {data}")
                return data
