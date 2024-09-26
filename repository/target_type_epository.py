from returns.result import Result, Success, Failure
from returns.maybe import Maybe, Nothing
from sqlalchemy.exc import SQLAlchemyError
from models import TargetType
from config.base import session_factory


def find_target_type_by_name(target_type_name: str) -> Maybe[TargetType]:
    with session_factory() as session:
        return Maybe.from_optional(
            session.query(TargetType).filter(TargetType.target_type_name == target_type_name).first())


def is_target_type_exist(target_type_name: str) -> bool:
    return find_target_type_by_name(target_type_name) is not Nothing


def insert_target_type(target_type: TargetType) -> Result[TargetType, str]:
    if find_target_type_by_name(target_type.target_type_name) is not Nothing:
        return Failure(f'Error: TargetType with name: {target_type.target_type_name} already exists')

    with session_factory() as session:
        try:
            session.add(target_type)
            session.commit()
            session.refresh(target_type)
            return Success(target_type)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(f'Error creating target type: {str(e)}')


def update_target_type_by_id(target_type_id: int, target_type: TargetType) -> Result[TargetType, str]:
    with session_factory() as session:
        try:
            existing_target_type = session.query(TargetType).filter(
                TargetType.target_type_id == target_type_id).first()
            if not existing_target_type:
                return Failure(f'Error: TargetType with id: {target_type.target_type_id} not found')

            for key, value in target_type.__dict__.items():
                if key != 'target_type_id' and value is not None:
                    setattr(existing_target_type, key, value)

            session.commit()
            session.refresh(existing_target_type)
            return Success(existing_target_type)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(f'Error updating target type: {str(e)}')


def delete_target_type_by_id(target_type_id: int) -> Result[bool, str]:
    with session_factory() as session:
        try:
            target_type = session.query(TargetType).filter(TargetType.target_type_id == target_type_id).first()
            if not target_type:
                return Failure(f'Error: TargetType with id: {target_type_id} not found')

            session.delete(target_type)
            session.commit()
            return Success(True)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(f'Error deleting target type: {str(e)}')


def get_target_type_by_id(target_type_id: int) -> Maybe[TargetType]:
    with session_factory() as session:
        return Maybe.from_optional(
            session.query(TargetType).filter(TargetType.target_type_id == target_type_id).first())


def get_all_target_types() -> Result[list[TargetType], str]:
    with session_factory() as session:
        try:
            target_types = session.query(TargetType).all()
            return Success(target_types)
        except SQLAlchemyError as e:
            return Failure(f'Error retrieving target types: {str(e)}')
