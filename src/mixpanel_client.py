import os
import json
from datetime import datetime
from typing import Dict, List

import requests

from src.models import UserEvent, EventType


def _to_datetime(value: object) -> datetime:
    if isinstance(value, (int, float)):
        # Mixpanel export often returns epoch seconds in properties["time"]
        return datetime.utcfromtimestamp(int(value))
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            pass
    return datetime.utcnow()


def _map_event_name_to_type(event_name: str) -> EventType:
    name = (event_name or "").lower()
    if "view" in name:
        return EventType.VIEWED
    if "save" in name:
        return EventType.SAVED
    if "complete" in name or "finish" in name:
        return EventType.COMPLETED
    if "start" in name or "begin" in name:
        return EventType.STARTED
    if "like" in name or "thumb" in name:
        return EventType.LIKED
    return EventType.VIEWED


def fetch_user_events(
    user_id: str,
    from_date: str,
    to_date: str,
    event_names: List[str],
    api_secret: str,
) -> List[UserEvent]:
    params: Dict[str, str] = {
        "from_date": from_date,
        "to_date": to_date,
        "event": json.dumps(event_names),
        "where": json.dumps({"properties[\"distinct_id\"]": user_id}),
    }

    url = "https://data.mixpanel.com/api/2.0/export/"
    response = requests.get(url, params=params, auth=(api_secret, ""), timeout=60)
    response.raise_for_status()

    events: List[UserEvent] = []
    for line in response.iter_lines():
        if not line:
            continue
        try:
            payload = json.loads(line.decode("utf-8"))
        except Exception:
            continue

        properties: Dict = payload.get("properties", {}) or {}
        if properties.get("distinct_id") != user_id:
            # Extra guard if filter is ignored
            continue

        event_name: str = payload.get("event", "")
        event_type = _map_event_name_to_type(event_name)

        tutorial_id = str(properties.get("tutorial_id") or properties.get("content_id") or "unknown")
        tags = properties.get("tags") or []
        tools = properties.get("tools") or []

        timestamp = _to_datetime(properties.get("time") or properties.get("$time") or properties.get("mp_processing_time_ms"))

        events.append(
            UserEvent(
                user_id=user_id,
                tutorial_id=tutorial_id,
                event_type=event_type,
                timestamp=timestamp,
                tags=list(tags) if isinstance(tags, list) else [],
                tools=list(tools) if isinstance(tools, list) else [],
            )
        )

    return events


