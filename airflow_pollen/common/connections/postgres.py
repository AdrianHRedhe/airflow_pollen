import os
from types import SimpleNamespace

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def Postgres():
    load_dotenv()
    # Load connection params from env
    url = (
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )

    engine = create_engine(url, pool_pre_ping=True)

    def execute_query(engine, query, params=None):
        with engine.begin() as conn:
            conn.execute(text(query), params or {})

    def fetch_query(engine, query, params=None):
        with engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]

    return SimpleNamespace(
        fetch_query=fetch_query, execute_query=execute_query, engine=engine
    )


postgres = Postgres()
