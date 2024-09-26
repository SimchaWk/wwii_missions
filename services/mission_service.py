from typing import List, Dict
from returns.maybe import Some
from returns.result import Result, Success, Failure

from config.base import session_factory
from repository.mission_repository import get_all_missions, get_mission_by_id


def get_mission_dict(mission: Dict) -> Dict:
    return {
        'mission_id': mission.get('mission_id'),
        'mission_date': mission.get('mission_date'),
        'air_force': mission.get('air_force'),
        'country': mission.get('country'),
        'target_city': mission.get('target_city'),
        'target_type': mission.get('target_type'),
        'aircraft_series': mission.get('aircraft_series'),
        'takeoff_base': mission.get('takeoff_base'),
        'target_priority': mission.get('target_priority')
    }


def get_mission(mission_id: int) -> Result[Dict, str]:
    with session_factory() as session:
        try:
            mission_maybe = get_mission_by_id(session, mission_id)
            if isinstance(mission_maybe, Some):
                return Success(get_mission_dict(mission_maybe.unwrap()))
            return Failure(f"Mission with id {mission_id} not found")
        except Exception as e:
            return Failure(f"Error retrieving mission: {str(e)}")


def get_all_missions_service() -> Result[List[Dict], str]:
    with session_factory() as session:
        try:
            missions_maybe = get_all_missions(session)
            return Success([get_mission_dict(mission) for mission in missions_maybe.unwrap()])
        except Exception as e:
            return Failure(f"Failed to retrieve missions: {str(e)}")
