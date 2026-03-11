import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_ENV = ROOT_DIR / "src" / "clinica_backend" / ".env"
SQL_DIR = ROOT_DIR / "src" / "sql" / "olap"

load_dotenv(BACKEND_ENV)


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        dbname=os.getenv("DB_NAME", "clinica_prime"),
    )


def apply_sql_file(cur, sql_path: Path):
    sql = sql_path.read_text(encoding="utf-8")
    cur.execute(sql)


def main():
    files = [
        SQL_DIR / "001_create_olap_schema.sql",
        SQL_DIR / "002_refresh_olap.sql",
    ]

    for f in files:
        if not f.exists():
            raise FileNotFoundError(f"No existe el archivo SQL: {f}")

    with get_conn() as conn:
        with conn.cursor() as cur:
            for f in files:
                apply_sql_file(cur, f)
                print(f"Aplicado: {f.name}")
        conn.commit()

    print("Setup OLAP completado.")


if __name__ == "__main__":
    main()
