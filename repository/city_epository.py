from returns.result import Result, Success, Failure
from returns.maybe import Maybe, Nothing
from sqlalchemy.exc import SQLAlchemyError
from models import City

from config.base import session_factory


def find_city_by_name(name: str) -> Maybe[City]:
    with session_factory() as session:
        return Maybe.from_optional(session.query(City).filter(City.city_name == name).first())


def is_city_exist(city_name: str) -> bool:
    return find_city_by_name(city_name) is not Nothing


def insert_city(city: City) -> Result[City, str]:
    if find_city_by_name(city.city_name) is not Nothing:
        return Failure(f'Error: City with name: {city.city_name} already exists')

    with session_factory() as session:
        try:
            session.add(city)
            session.commit()
            session.refresh(city)
            return Success(city)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(f'Error creating city: {str(e)}')


def update_city_by_id(city_id: int, city: City) -> Result[City, str]:
    with session_factory() as session:
        try:
            existing_city = session.query(City).filter(City.city_id == city_id).first()
            if not existing_city:
                return Failure(f'Error: City with id: {city.city_id} not found')

            for key, value in city.__dict__.items():
                if key != 'city_id' and value is not None:
                    setattr(existing_city, key, value)

            session.commit()
            session.refresh(existing_city)
            return Success(existing_city)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(f'Error updating city: {str(e)}')


def delete_city_by_id(city_id: int) -> Result[bool, str]:
    with session_factory() as session:
        try:
            city = session.query(City).filter(City.city_id == city_id).first()
            if not city:
                return Failure(f'Error: City with id: {city_id} not found')

            session.delete(city)
            session.commit()
            return Success(True)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(f'Error deleting city: {str(e)}')


def get_city_by_id(city_id: int) -> Maybe[City]:
    with session_factory() as session:
        return Maybe.from_optional(session.query(City).filter(City.city_id == city_id).first())


def get_all_cities() -> Result[list[City], str]:
    with session_factory() as session:
        try:
            cities = session.query(City).all()
            return Success(cities)
        except SQLAlchemyError as e:
            return Failure(f'Error retrieving cities: {str(e)}')
