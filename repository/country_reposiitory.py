from returns.result import Result, Success, Failure
from returns.maybe import Maybe, Nothing
from sqlalchemy.exc import SQLAlchemyError

from config.base import session_factory
from models import Country


def find_country_by_id(country_id: int) -> Maybe[Country]:
    with session_factory() as session:
        return Maybe.from_optional(
            session.get(Country, country_id)
        )


def find_country_by_name(country_name: str) -> Maybe[Country]:
    with session_factory() as session:
        return Maybe.from_optional(session.query(Country).filter(Country.country_name == country_name).first())


def is_country_exist(country_name: str) -> bool:
    return find_country_by_name(country_name) is not Nothing


def insert_country(country: Country) -> Result[Country, str]:
    if find_country_by_name(country.country_name) is not Nothing:
        return Failure(f'Error: Country with name: {country.country_name} already exists')

    with session_factory() as session:
        try:
            session.add(country)
            session.commit()
            session.refresh(country)
            return Success(country)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(f'Error creating country: {str(e)}')


def update_country_by_id(country_id: int, country: Country) -> Result[Country, str]:
    with session_factory() as session:
        try:
            existing_country = session.query(Country).filter(Country.country_id == country_id).first()
            if not existing_country:
                return Failure(f'Error: Country with id: {country.country_id} not found')

            for key, value in country.__dict__.items():
                if key != 'country_id' and value is not None:
                    setattr(existing_country, key, value)

            session.commit()
            session.refresh(existing_country)
            return Success(existing_country)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(f'Error updating country: {str(e)}')


def delete_country_by_id(country_id: int) -> Result[bool, str]:
    with session_factory() as session:
        try:
            country = session.query(Country).filter(Country.country_id == country_id).first()
            if not country:
                return Failure(f'Error: Country with id: {country_id} not found')

            session.delete(country)
            session.commit()
            return Success(True)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(f'Error deleting country: {str(e)}')


def get_all_countries() -> Result[list[Country], str]:
    with session_factory() as session:
        try:
            countries = session.query(Country).all()
            return Success(countries)
        except SQLAlchemyError as e:
            return Failure(f'Error retrieving countries: {str(e)}')
