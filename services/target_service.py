from models import Target
from repository.target_epository import *
from returns.result import Result, Success, Failure
from returns.maybe import Nothing, Some
from dictalchemy.utils import asdict
from toolz import curry


def convert_to_target(data: dict) -> Result[Target, str]:
    if not all(key in data for key in ['target_industry', 'city_id']):
        return Failure("Missing required fields: 'target_industry' or 'city_id'")

    target = Target(
        target_industry=data.get('target_industry'),
        city_id=data.get('city_id'),
        target_type_id=data.get('target_type_id'),
        target_priority=data.get('target_priority')
    )
    return Success(target)


def create_target(data: dict) -> Result[dict, str]:
    target_result = convert_to_target(data)

    if isinstance(target_result, Success):
        target = target_result.unwrap()
        result = insert_target(target)
        if isinstance(result, Success):
            return Success(asdict(target))
        return Failure("Failed to insert target into the database")

    return Failure(target_result.failure())


def update_target(target_id: int, data: dict) -> Result[dict, str]:
    target_result = get_target_by_id(target_id)

    if isinstance(target_result, Some):
        target = target_result.unwrap()

        target.target_industry = data.get('target_industry', target.target_industry)
        target.city_id = data.get('city_id', target.city_id)
        target.target_type_id = data.get('target_type_id', target.target_type_id)
        target.target_priority = data.get('target_priority', target.target_priority)

        result = update_target_by_id(target_id, target)
        if isinstance(result, Success):
            return Success(asdict(target))
        return Failure("Failed to update target in the database")

    return Failure(f"Target with id {target_id} not found")


def delete_target(target_id: int) -> Result[None, str]:
    target_result = get_target_by_id(target_id)

    if isinstance(target_result, Some):
        result = delete_target_by_id(target_id)
        if isinstance(result, Success):
            return Success(None)
        return Failure("Failed to delete target from the database")

    return Failure(f"Target with id {target_id} not found")


@curry
def filter_targets_by_industry(industry_pattern: str, targets: list[Target]) -> list[Target]:
    return [target for target in targets if industry_pattern.lower() in target.target_industry.lower()]


def get_targets_by_industry_pattern(industry_pattern: str) -> Result[list[dict], str]:
    targets_result = get_all_targets()

    if isinstance(targets_result, Success):
        filtered_targets = filter_targets_by_industry(industry_pattern)(targets_result.unwrap())
        return Success([asdict(target) for target in filtered_targets])

    return Failure("Failed to retrieve targets from the database")


@curry
def filter_targets_by_priority(priority: int, targets: list[Target]) -> list[Target]:
    return [target for target in targets if target.target_priority == priority]


def get_targets_by_priority(priority: int) -> Result[list[dict], str]:
    targets_result = get_all_targets()

    if isinstance(targets_result, Success):
        filtered_targets = filter_targets_by_priority(priority)(targets_result.unwrap())
        return Success([asdict(target) for target in filtered_targets])

    return Failure("Failed to retrieve targets from the database")
