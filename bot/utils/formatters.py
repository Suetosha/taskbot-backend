from .time_utils import datetime_to_iso


def render_task(task: dict, category_map: dict[str, str]) -> str:
    title = task.get("title") or "Без названия"
    status = "выполнено" if task.get("is_completed") else "не выполнено"

    cats = task.get("categories") or []
    cat_names = [category_map.get(str(cid), str(cid)) for cid in cats]
    cats_text = ", ".join(cat_names) if cat_names else "—"

    return (
        f"• {title}\n"
        f"  Статус: {status}\n"
        f"  Создано: {datetime_to_iso(task.get('created_at'))}\n"
        f"  Срок: {datetime_to_iso(task.get('due_at'))}\n"
        f"  Категории: {cats_text}"
    )
