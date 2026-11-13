from datetime import datetime, timezone

def is_observation_stale(source_timestamp: datetime, max_age_hours: int = 24) -> bool:
    stamp = source_timestamp.replace(tzinfo=timezone.utc) if source_timestamp.tzinfo is None else source_timestamp
    return (datetime.now(timezone.utc) - stamp).total_seconds() > max_age_hours * 3600
