from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:1234@localhost/wwii_missions')
# use session_factory() to get a new Session
_session_factory = sessionmaker(bind=engine)

Base = declarative_base()


def session_factory():
    Base.metadata.create_all(engine)
    return _session_factory()


def create_database_if_not_exists():
    if not database_exists(engine.url):
        create_database(engine.url)


def drop_all_tables():
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception as e:
        print(f"Error occurred while dropping tables: {str(e)}")

