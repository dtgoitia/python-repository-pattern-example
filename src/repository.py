from typing import Dict, List

import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.orm.session import Session, sessionmaker
from sqlalchemy.sql.expression import column, select
from sqlalchemy.sql.schema import MetaData, Table

from src import model
from src.config import get_config

config = get_config()
engine: Engine = create_engine(f"sqlite:///{config.database_uri}", echo=config.debug)


mapper_registry = sqlalchemy.orm.registry()
# 'metadata' will hold in-memory the information of all tables
metadata: MetaData = mapper_registry.metadata

account_table = Table(
    "accounts",
    metadata,
    Column("id", String, primary_key=True, nullable=False),
    Column("name", String, nullable=False),
)

transaction_table = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("from_account_id", ForeignKey("accounts.id"), nullable=False),
    # Column("to_account", ForeignKey("accounts.id"), nullable=False),
    Column("quantity", Integer, nullable=False),
)

# TODO: can I bind session instead of engine? the session wraps an Engine and
# Connections, right? There must be a way
metadata.bind = engine
metadata.create_all(checkfirst=True)


def start_mappers():
    """Mappers must be initialized before any domain instance is read or written.

    The reason is that the mapping initialization modifies the domain model class, so
    that the domain model class becomes aware of the persistence layer (only on runtime).
    """

    mapper_registry.map_imperatively(
        model.Account,
        account_table,
        properties={
            "transactions": relationship(model.Transaction, backref="from_account")
        },
    )

    mapper_registry.map_imperatively(model.Transaction, transaction_table)


class Repository:
    def __init__(self, session: Session) -> None:
        # self._engine = engine
        # TODO: do you need to do any assertions?
        self._session = session

        start_mappers()

    def add_account(self, account: model.Account) -> None:
        self._session.add(account)
        self._session.commit()

    def add_transaction(self, transaction: model.Transaction) -> None:
        self._session.add(transaction)
        self._session.commit()

    def read_accounts(self) -> List[model.Account]:
        query = select(model.Account)
        # ToDo: perhaps return an iterator (lazy-loaded)
        accounts = [account[0] for account in self._session.execute(query).all()]
        return accounts

    def read_transactions(self) -> List[model.Transaction]:
        query = select(model.Transaction)
        # ToDo: perhaps return an iterator (lazy-loaded)
        transactions = [
            transaction[0] for transaction in self._session.execute(query).all()
        ]
        return transactions


def create_session(engine: Engine) -> Session:
    SessionClass = sessionmaker(
        bind=engine,
        # to be compatible with SQLAlchemy 2.0
        # https://docs.sqlalchemy.org/en/14/orm/session_basics.html#querying-2-0-style
        future=True,
    )
    session_instance: Session = SessionClass()
    return session_instance
