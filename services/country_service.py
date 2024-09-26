from models import Country
from repository.country_reposiitory import *
from returns.result import Result, Success, Failure
from returns.maybe import Nothing, Some
from dictalchemy.utils import asdict
from toolz import curry


def convert_to_country(data: dict) -> Result[Country, str]:
    if not data.get('country_name'):
        return Failure("Missing required field: 'country_name'")

    if find_country_by_name(data.get('country_name')) is not Nothing:
        return Failure(f"Country with name {data.get('country_name')} already exists")

    country = Country(country_name=data.get('country_name'))
    return Success(country)


def create_country(data: dict) -> Result[dict, str]:
    country_result = convert_to_country(data)

    if isinstance(country_result, Success):
        country = country_result.unwrap()
        result = insert_country(country)
        if isinstance(result, Success):
            return Success(asdict(country))
        return Failure("Failed to insert country into the database")

    return Failure(country_result.failure())


def update_country(country_id: int, data: dict) -> Result[dict, str]:
    country_result = find_country_by_id(country_id)

    if isinstance(country_result, Some):
        country = country_result.unwrap()

        country.country_name = data.get('country_name', country.country_name)

        result = update_country_by_id(country_id, country)
        if isinstance(result, Success):
            return Success(asdict(country))
        return Failure("Failed to update country in the database")

    return Failure(f"Country with id {country_id} not found")


def delete_country(country_id: int) -> Result[bool, str]:
    country_result = find_country_by_id(country_id)

    if isinstance(country_result, Some):
        result = delete_country_by_id(country_id)
        if isinstance(result, Success):
            return Success(bool)
        return Failure("Failed to delete country from the database")

    return Failure(f"Country with id {country_id} not found")


@curry
def filter_countries_by_name(name_pattern: str, countries: list[Country]) -> list[Country]:
    return [country for country in countries if name_pattern.lower() in country.country_name.lower()]


def get_countries_by_name_pattern(name_pattern: str) -> Result[list[dict], str]:
    countries_result = get_all_countries()

    if isinstance(countries_result, Success):
        filtered_countries = filter_countries_by_name(name_pattern)(countries_result.unwrap())
        return Success([asdict(country) for country in filtered_countries])

    return Failure("Failed to retrieve countries from the database")
