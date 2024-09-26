from models import TargetType
from repository.target_type_epository import *
from returns.result import Result, Success, Failure
from returns.maybe import Nothing, Some
from dictalchemy.utils import asdict
from toolz import curry


def convert_to_target_type(data: dict) -> Result[TargetType, str]:
    if find_target_type_by_name(data.get('target_type_name')) is not Nothing:
        return Failure(f"Target Type with name {data.get('target_type_name')} already exists")

    target_type = TargetType(
        target_type_name=data.get('target_type_name')
    )
    return Success(target_type)


def create_target_type(data: dict) -> Result[dict, str]:
    target_type_result = convert_to_target_type(data)

    if isinstance(target_type_result, Success):
        target_type = target_type_result.unwrap()
        result = insert_target_type(target_type)
        if isinstance(result, Success):
            return Success(asdict(target_type))
        return Failure("Failed to insert target type into the database")

    return Failure(target_type_result.failure())


def update_target_type(target_type_id: int, data: dict) -> Result[dict, str]:
    target_type_result = get_target_type_by_id(target_type_id)

    if isinstance(target_type_result, Some):
        target_type = target_type_result.unwrap()

        target_type.target_type_name = data.get('target_type_name', target_type.target_type_name)

        result = update_target_type_by_id(target_type_id, target_type)
        if isinstance(result, Success):
            return Success(asdict(target_type))
        return Failure("Failed to update target type in the database")

    return Failure(f"Target Type with id {target_type_id} not found")


def delete_target_type(target_type_id: int) -> Result[bool, str]:
    target_type_result = get_target_type_by_id(target_type_id)

    if isinstance(target_type_result, Some):
        result = delete_target_type_by_id(target_type_id)
        if isinstance(result, Success):
            return Success(True)
        return Failure("Failed to delete target type from the database")

    return Failure(f"Target Type with id {target_type_id} not found")


@curry
def filter_target_types_by_name(name_pattern: str, target_types: list[TargetType]) -> list[TargetType]:
    return [tt for tt in target_types if name_pattern.lower() in tt.target_type_name.lower()]


def get_target_types_by_name_pattern(name_pattern: str) -> Result[list[dict], str]:
    target_types_result = get_all_target_types()

    if isinstance(target_types_result, Success):
        filtered_target_types = filter_target_types_by_name(name_pattern)(target_types_result.unwrap())
        return Success([asdict(tt) for tt in filtered_target_types])

    return Failure("Failed to retrieve target types from the database")
