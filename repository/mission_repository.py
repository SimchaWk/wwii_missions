from typing import List, Dict, Optional
from sqlalchemy import text
from returns.maybe import Maybe, Some, Nothing


def get_all_missions(session) -> Maybe[List[Dict]]:
    result = session.execute(text("SELECT * FROM mission"))
    return Some([dict(row._mapping) for row in result]) if result else Nothing


def get_mission_by_id(session, mission_id: int) -> Maybe[Dict]:
    result = session.execute(text("SELECT * FROM mission WHERE mission_id = :id"), {"id": mission_id})
    row = result.fetchone()
    return Some(dict(row._mapping)) if row else Nothing
