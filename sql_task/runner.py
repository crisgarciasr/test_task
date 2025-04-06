from pathlib import Path
from random import choice

from rich import print
from rich.pretty import pprint
from sqlalchemy import text

try:
    from .data_generator import DATABASE_URI, db_session
except ImportError:
    from data_generator import DATABASE_URI, db_session

columns = [
    "client_id",
    "history_average_loan_profit_margin_l12m",
    "history_payment_delay_flag_l6m",
    "history_payment_ratio_l9m_to_total",
    "vendor_grocery_utilities_transaction_ratio_l9m",
    "vendor_microfinance_gambling_payment_ratio_l12m",
]


def run_once():
    query_path = Path(__file__).parent / "query.sql"
    if not query_path.exists():
        raise FileNotFoundError(f"Query file not found at {query_path.resolve()}")

    with open(query_path, "r", encoding="utf-8") as file:
        query = text(file.read())

    with db_session(DATABASE_URI) as session:
        # Get all clients
        clients = session.execute(text("SELECT id FROM clients")).fetchall()
        # Select a random client
        params = {
            "client_id": choice(clients)[0],
        }
        # Execute the query with the selected client and get the result as a dictionary
        result = dict(session.execute(query, params).mappings().one())

        # Print the result
        print()
        print(f"[bold]Query executed with parameters: {params}")

        # Warn if any column is missing
        missing_columns = set(columns) - set(result.keys())
        if missing_columns:
            print(f"[bold yellow]\nMissing columns in the result:")
            pprint(missing_columns)
        # Warn if any column is extra
        extra_columns = set(result.keys()) - set(columns)
        if extra_columns:
            print(f"[bold yellow]\nExtra columns in the result:")
            pprint(extra_columns)

        # Warn if any column is None

        # Print the result
        print("[bold]\nQuery result:")
        pprint(result)


if __name__ == "__main__":
    run_once()
