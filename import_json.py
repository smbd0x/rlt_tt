import json
from dateutil import parser

from config import Config
from db.base import SessionLocal
from db.models import Video, VideoSnapshot

DATABASE_URL = Config.DATABASE_URL
JSON_FILE = "videos.json"


def parse_dt(dt_str: str):
    if not dt_str:
        return None
    dt = parser.isoparse(dt_str)
    return dt.replace(tzinfo=None)


async def import_json():

    with open(JSON_FILE, "r", encoding="utf8") as f:
        data = json.load(f)

    videos = data["videos"]
    print(f"Найдено {len(videos)} видео")

    async with SessionLocal() as session:
        async with session.begin():

            for v in videos:
                video = Video(
                    id=v["id"],
                    creator_id=v["creator_id"],
                    video_created_at=parse_dt(v["video_created_at"]),
                    views_count=v.get("views_count"),
                    likes_count=v.get("likes_count"),
                    comments_count=v.get("comments_count"),
                    reports_count=v.get("reports_count"),
                    created_at=parse_dt(v.get("created_at")),
                    updated_at=parse_dt(v.get("updated_at")),
                )

                session.add(video)

                for s in v.get("snapshots", []):
                    snap = VideoSnapshot(
                        id=s["id"],
                        video_id=s["video_id"],
                        views_count=s.get("views_count"),
                        likes_count=s.get("likes_count"),
                        comments_count=s.get("comments_count"),
                        reports_count=s.get("reports_count"),
                        delta_views_count=s.get("delta_views_count"),
                        delta_likes_count=s.get("delta_likes_count"),
                        delta_comments_count=s.get("delta_comments_count"),
                        delta_reports_count=s.get("delta_reports_count"),
                        created_at=parse_dt(s.get("created_at")),
                        updated_at=parse_dt(s.get("updated_at")),
                    )
                    session.add(snap)

        await session.commit()

    print("🎉 Готово! Данные успешно импортированы.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(import_json())
