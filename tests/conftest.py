import pytest
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm.session import Session

from src.config import AppConfig, get_config
from src.repository import create_tables


@pytest.fixture(scope="session")
def config() -> AppConfig:
    return get_config()


@pytest.fixture(scope="session")
def engine(config: AppConfig) -> Engine:
    """Returns an SQLAlchemy engine pointing to an in-memory SQLite.

    This avoid contaminating the production DB.
    """

    in_memory_db_url = "sqlite://"
    engine: Engine = create_engine(in_memory_db_url, echo=config.debug)

    # The in-memory DB is still empty
    create_tables(engine)

    return engine


@pytest.fixture(scope="function")
def session(engine: Engine) -> Session:
    """Returns a Session instance that rolls changes back after every test."""

    session = Session(engine)

    # flush = notify changes to DB, but don't end transaction
    # commit = notify changes to DB, and end transaction (can't be rolled back)
    session.commit = session.flush

    session.begin()
    yield session

    # These lines will be executed even if the test failed
    session.rollback()
    session.close()
