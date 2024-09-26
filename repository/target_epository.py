from returns.result import Result, Success, Failure
from returns.maybe import Maybe
from sqlalchemy.exc import SQLAlchemyError
from models import Target
from config.base import session_factory


def insert_target(target: Target) -> Result[Target, str]:
    with session_factory() as session:
        try:
            session.add(target)
            session.commit()
            session.refresh(target)
            return Success(target)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(f'Error creating target: {str(e)}')


def update_target_by_id(target_id: int, target: Target) -> Result[Target, str]:
    with session_factory() as session:
        try:
            existing_target = session.query(Target).filter(Target.target_id == target_id).first()
            if not existing_target:
                return Failure(f'Error: Target with id: {target.target_id} not found')

            for key, value in target.__dict__.items():
                if key != 'target_id' and value is not None:
                    setattr(existing_target, key, value)

            session.commit()
            session.refresh(existing_target)
            return Success(existing_target)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(f'Error updating target: {str(e)}')


def delete_target_by_id(target_id: int) -> Result[bool, str]:
    with session_factory() as session:
        try:
            target = session.query(Target).filter(Target.target_id == target_id).first()
            if not target:
                return Failure(f'Error: Target with id: {target_id} not found')

            session.delete(target)
            session.commit()
            return Success(True)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(f'Error deleting target: {str(e)}')


def get_target_by_id(target_id: int) -> Maybe[Target]:
    with session_factory() as session:
        return Maybe.from_optional(session.query(Target).filter(Target.target_id == target_id).first())


def get_all_targets() -> Result[list[Target], str]:
    with session_factory() as session:
        try:
            targets = session.query(Target).all()
            return Success(targets)
        except SQLAlchemyError as e:
            return Failure(f'Error retrieving targets: {str(e)}')
