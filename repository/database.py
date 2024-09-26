from config.base import engine, Base, create_database_if_not_exists, drop_all_tables
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import text, inspect

from config.base import session_factory
from models import City, Country, Target, TargetType


def create_tables():
    Base.metadata.create_all(engine)


def normalize_data():
    with session_factory() as session:
        inspector = inspect(engine)
        if not inspector.has_table('mission'):
            print("Table 'mission' does not exist. Please make sure it's created and populated with data.")
            return

        original_data = session.execute(text("SELECT * FROM mission")).fetchall()

        for index, row in enumerate(original_data):
            try:
                # Country
                country_name = row.target_country if row.target_country else "Unknown"
                country = session.query(Country).filter_by(country_name=country_name).first()
                if not country:
                    country = Country(country_name=country_name)
                    session.add(country)
                    session.flush()

                # City
                city_name = row.target_city if row.target_city else "Unknown"
                city = session.query(City).filter_by(city_name=city_name).first()
                if not city:
                    city = City(
                        city_name=city_name,
                        country_id=country.country_id,
                        latitude=row.target_latitude if row.target_latitude else None,
                        longitude=row.target_longitude if row.target_longitude else None
                    )
                    session.add(city)
                    session.flush()

                # TargetType
                target_type_name = row.target_type if row.target_type else "Unknown"
                target_type = session.query(TargetType).filter_by(target_type_name=target_type_name).first()
                if not target_type:
                    target_type = TargetType(target_type_name=target_type_name)
                    session.add(target_type)
                    session.flush()

                # Target
                target_priority = None
                if row.target_priority:
                    try:
                        target_priority = int(row.target_priority)
                    except ValueError:
                        print(f"Invalid target_priority value '{row.target_priority}' for row {index+1}. Setting to None.")

                target = Target(
                    target_industry=row.target_industry if row.target_industry else "Unknown",
                    city_id=city.city_id,
                    target_type_id=target_type.target_type_id,
                    target_priority=target_priority
                )
                session.add(target)

                if index % 1000 == 0:
                    print(f"Processed {index+1} rows")
                    session.commit()

            except Exception as e:
                print(f"Error processing row {index+1}: {str(e)}")
                session.rollback()

        print("Data normalization completed successfully.")


if __name__ == "__main__":
    create_database_if_not_exists()
    # drop_all_tables()  # זהירות: זה ימחק את כל הטבלאות הקיימות
    create_tables()
    normalize_data()
