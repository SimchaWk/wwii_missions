from models import City
from repository.city_epository import *
from returns.result import Result, Success, Failure
from returns.maybe import Nothing, Some
from dictalchemy.utils import asdict
from toolz import curry


def convert_to_city(data: dict) -> Result[City, str]:
    if not data.get('city_name'):
        return Failure("Missing required field: 'city_name'")

    if find_city_by_name(data.get('city_name')) is not Nothing:
        return Failure(f"City with name {data.get('city_name')} already exists")

    city = City(
        city_name=data.get('city_name'),
        country_id=data.get('country_id'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )
    return Success(city)


def create_city(data: dict) -> Result[dict, str]:
    city_result = convert_to_city(data)

    if isinstance(city_result, Success):
        city = city_result.unwrap()
        result = insert_city(city)
        if isinstance(result, Success):
            return Success(asdict(city))
        return Failure("Failed to insert city into the database")

    return Failure(city_result.failure())


def update_city(city_id: int, data: dict) -> Result[dict, str]:
    city_result = get_city_by_id(city_id)

    if isinstance(city_result, Some):
        city = city_result.unwrap()

        city.city_name = data.get('city_name', city.city_name)
        city.country_id = data.get('country_id', city.country_id)
        city.latitude = data.get('latitude', city.latitude)
        city.longitude = data.get('longitude', city.longitude)

        result = update_city_by_id(city_id, city)
        if isinstance(result, Success):
            return Success(asdict(city))
        return Failure("Failed to update city in the database")

    return Failure(f"City with id {city_id} not found")


def delete_city(city_id: int) -> Result[bool, str]:
    city_result = get_city_by_id(city_id)

    if isinstance(city_result, Some):
        result = delete_city_by_id(city_id)
        if isinstance(result, Success):
            return Success(True)
        return Failure("Failed to delete city from the database")

    return Failure(f"City with id {city_id} not found")


@curry
def filter_cities_by_name(name_pattern: str, cities: list[City]) -> list[City]:
    return [city for city in cities if name_pattern.lower() in city.city_name.lower()]


def get_cities_by_name_pattern(name_pattern: str) -> Result[list[dict], str]:
    cities_result = get_all_cities()

    if isinstance(cities_result, Success):
        filtered_cities = filter_cities_by_name(name_pattern)(cities_result.unwrap())
        return Success([asdict(city) for city in filtered_cities])

    return Failure("Failed to retrieve cities from the database")


@curry
def filter_cities_by_country(country_id: int, cities: list[City]) -> list[City]:
    return [city for city in cities if city.country_id == country_id]


def get_cities_by_country(country_id: int) -> Result[list[dict], str]:
    cities_result = get_all_cities()

    if isinstance(cities_result, Success):
        filtered_cities = filter_cities_by_country(country_id)(cities_result.unwrap())
        return Success([asdict(city) for city in filtered_cities])

    return Failure("Failed to retrieve cities from the database")
