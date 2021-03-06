from typing import List

import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.schema import MetaData, Table

from src import model
from src.config import get_config

config = get_config()
engine: Engine = create_engine(config.database_uri, echo=config.debug)


mapper_registry = sqlalchemy.orm.registry()
# 'metadata' will hold in-memory the information of all tables
metadata: MetaData = mapper_registry.metadata

# latest schema
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
    Column("to_account_id", ForeignKey("accounts.id"), nullable=False),
    Column("quantity", Integer, nullable=False),
)

# Let SQLAlchemy know which SQL flavour shuold be used to build the tables
metadata.bind = engine


def create_tables(engine: Engine) -> None:
    metadata.create_all(engine, checkfirst=True)


def start_mappers():
    """Mappers must be initialized before any domain instance is read or written.

    The reason is that the mapping initialization modifies the domain model class, so
    that the domain model class becomes aware of the persistence layer - only on runtime
    """

    mapper_registry.map_imperatively(
        model.Account,
        account_table,
        properties={
            "transactions_out": relationship(
                model.Transaction,
                backref="from_account",
                foreign_keys=transaction_table.columns.from_account_id,
            ),
            "transactions_in": relationship(
                model.Transaction,
                backref="to_account",
                foreign_keys=transaction_table.columns.to_account_id,
            ),
        },
    )

    mapper_registry.map_imperatively(model.Transaction, transaction_table)


class Repository:
    _orm_mappers_initialized = False

    def __init__(self, session: Session) -> None:
        self._session = session
        self._start_mappers()

    @classmethod
    def _start_mappers(cls) -> None:
        """On runtime, mappers must only be initialized once."""
        if cls._orm_mappers_initialized:
            return

        start_mappers()
        cls._orm_mappers_initialized = True

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
    session = Session(
        bind=engine,
        # to be compatible with SQLAlchemy 2.0
        # https://docs.sqlalchemy.org/en/14/orm/session_basics.html#querying-2-0-style
        future=True,
    )
    return session
