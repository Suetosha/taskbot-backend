from datetime import datetime
from zoneinfo import ZoneInfo

ADAK_TZ = ZoneInfo("America/Adak")


def parse_user_datetime(text: str) -> str | None:
    raw = (text or "").strip()
    if raw == "-":
        return None

    try:
        dt = datetime.strptime(raw, "%d.%m.%Y %H:%M")
    except ValueError as e:
        raise ValueError(
            "Неверный формат. Введите ДД.ММ.ГГГГ ЧЧ:ММ или '-'"
        ) from e

    return dt.replace(tzinfo=ADAK_TZ).isoformat()


def datetime_to_iso(value: str | None) -> str:
    if not value:
        return "—"
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return value
