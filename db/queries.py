from dateutil import parser
from sqlalchemy import text
from db.base import SessionLocal


async def run_query(command: dict) -> int:
    action = command.get("action")
    print(f"Поступила новая команда: {command}")

    if action == "count_videos":
        return await count_videos(command.get("filters"))

    if action == "sum_delta":
        return await sum_delta(command["metric"], command["date"])

    if action == "count_snapshot_events":
        return await count_snapshot_events(command["metric"], command["date"])

    if action == "custom_sql":
        return await run_custom_sql(command["sql"], command.get("params", {}))

    raise ValueError("Unknown action")


async def count_videos(filters: dict | None) -> int:
    async with SessionLocal() as session:
        base = "SELECT COUNT(*) FROM videos WHERE 1=1"
        params = {}

        if filters:
            if creator := filters.get("creator_id"):
                base += " AND creator_id = :creator_id"
                params["creator_id"] = creator

            if c_from := filters.get("created_from"):
                params["created_from"] = parser.parse(c_from)
                base += " AND video_created_at >= :created_from"

            if c_to := filters.get("created_to"):
                params["created_to"] = parser.parse(c_to)
                base += " AND video_created_at <= :created_to"

            if views_gt := filters.get("views_gt"):
                base += " AND views_count > :views_gt"
                params["views_gt"] = views_gt

            if likes_gt := filters.get("likes_gt"):
                base += " AND likes_count > :likes_gt"
                params["likes_gt"] = likes_gt

            if comments_gt := filters.get("comments_gt"):
                base += " AND comments_count > :comments_gt"
                params["comments_gt"] = comments_gt

            if reports_gt := filters.get("reports_gt"):
                base += " AND reports_count > :reports_gt"
                params["reports_gt"] = reports_gt

        result = await session.execute(text(base), params)
        return result.scalar_one()


async def sum_delta(metric: str, date: str) -> int:
    column = f"delta_{metric}_count"
    sql = f"""
        SELECT COALESCE(SUM({column}), 0)
        FROM video_snapshots
        WHERE DATE(created_at) = :date
    """
    async with SessionLocal() as session:
        date_obj = parser.parse(date).date()
        result = await session.execute(text(sql), {"date": date_obj})
        return result.scalar_one()


async def count_snapshot_events(metric: str, date: str) -> int:
    column = f"delta_{metric}_count"
    sql = f"""
        SELECT COUNT(DISTINCT video_id)
        FROM video_snapshots
        WHERE DATE(created_at) = :date AND {column} > 0
    """
    async with SessionLocal() as session:
        date_obj = parser.parse(date).date()
        result = await session.execute(text(sql), {"date": date_obj})
        return result.scalar_one()


async def run_custom_sql(sql: str, params: dict) -> int:
        for key, value in params.items():
            if isinstance(value, str):
                try:
                    params[key] = parser.parse(value)
                except Exception as e:
                    print(e)

        async with SessionLocal() as session:
            result = await session.execute(text(sql), params)
            return result.scalar_one()
