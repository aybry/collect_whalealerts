import os
import time
import logging
import sqlalchemy
import requests
import pandas as pd

from sqlalchemy import Column, Integer, String, Float, Table, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()

PG_WHALEALERT_HOST = os.getenv("PG_WHALEALERT_HOST")
PG_WHALEALERT_PORT = os.getenv("PG_WHALEALERT_PORT")
PG_WHALEALERT_DBNAME = os.getenv("PG_WHALEALERT_DBNAME")
PG_WHALEALERT_USER = os.getenv("PG_WHALEALERT_USER")
PG_WHALEALERT_PASSWORD = os.getenv("PG_WHALEALERT_PASSWORD")
WHALEALERT_API_KEY = os.getenv("WHALEALERT_API_KEY")

TRANSACTIONS_URL = (
    "https://api.whale-alert.io/v1/transactions?api_key={}&min_value=500000&start={}"
)


def main():
    ensure_table_exists()

    counter = 0
    while True:
        try:
            LOGGER.debug("Starting fetch")
            fetch_transactions()
            LOGGER.debug("Fetch successful")
            counter += 1
        except:
            LOGGER.error("Fetch unsuccessful...")
            LOGGER.exception("")

        LOGGER.debug("Sleeping...")
        time.sleep(20)
        LOGGER.debug(f"Fetched {counter} times")


def ensure_table_exists():
    if "transactions" in METADATA.tables:
        return

    table = Table(
        "transactions",
        METADATA,
        Column("id", Integer, primary_key=True),
        Column("timestamp", Integer),
        Column("blockchain", String),
        Column("symbol", String),
        Column("transaction_type", String),
        Column("hash", String),
        Column("from_address", String),
        Column("from_owner", String),
        Column("from_owner_type", String),
        Column("to_address", String),
        Column("to_owner", String),
        Column("to_owner_type", String),
        Column("amount", Float),
        Column("amount_usd", Float),
        Column("transaction_count", Integer),
    )

    table.create()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    blockchain = Column(String)
    symbol = Column(String)
    transaction_type = Column(String)
    hash = Column(String)
    from_address = Column(String)
    from_owner = Column(String)
    from_owner_type = Column(String)
    to_address = Column(String)
    to_owner = Column(String)
    to_owner_type = Column(String)
    amount = Column(Float)
    amount_usd = Column(Float)
    transaction_count = Column(Integer)

    def __repr__(self):
        return f"<Transaction {self.id}: {self.amount} {self.symbol} from {self.from_address[:10]}... to {self.to_address[:10]}...>"


def fetch_transactions():
    LOGGER.debug("Fetching...")

    r = requests.get(
        TRANSACTIONS_URL.format(WHALEALERT_API_KEY, int(time.time()) - 3599)
    )
    LOGGER.debug(f"Fetched transactions with response code {r.status_code}")

    if r.status_code == 200:
        tx_dictlist = pd.json_normalize(r.json()["transactions"], sep="_").to_dict(
            orient="records"
        )

        txs = [Transaction(**tx) for tx in tx_dictlist]

        LOGGER.debug(f"Fetched {len(tx_dictlist)} transactions")
        with SESSION() as session:
            tx_added = 0
            tx_skipped = 0
            for tx in txs:
                if (
                    len(
                        session.query(Transaction).filter(Transaction.id == tx.id).all()
                    )
                    == 1
                ):
                    tx_skipped += 1
                    continue

                try:
                    session.add(tx)
                    session.commit()
                    tx_added += 1
                except Exception as exc:
                    LOGGER.info(exc)

        LOGGER.info(f"Added {tx_added} rows, skipped {tx_skipped}")
    else:
        LOGGER.warning("Reponse was not valid.")


def init_logger():
    logger = logging.getLogger("whalealert")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("whalealert.log")
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


if __name__ == "__main__":
    LOGGER = init_logger()

    ENGINE = sqlalchemy.create_engine(
        "postgresql://"
        f"{PG_WHALEALERT_USER}:{PG_WHALEALERT_PASSWORD}"
        f"@{PG_WHALEALERT_HOST}:{PG_WHALEALERT_PORT}"
        f"/{PG_WHALEALERT_DBNAME}?sslmode=require"
    )
    METADATA = MetaData(ENGINE)
    METADATA.reflect(ENGINE)
    SESSION = sessionmaker(bind=ENGINE)

    main()
