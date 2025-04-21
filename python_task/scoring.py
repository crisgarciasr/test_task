import json
import os
from datetime import datetime
from python_task.src.models import Request, Response


def load_json(path):
    """
    Utility function to load a JSON file from a given path.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_pure_stream(request_id: str) -> bool:
    """
    Determines if the request_id falls into the 5% deterministic flow.
    Uses hash-based logic for reproducible randomness.
    """
    return hash(request_id) % 100 < 5


# ========== STRATEGY IMPLEMENTATIONS ==========

def apply_pure_stream(score: float) -> Response:
    """
    Pure Stream Strategy: Always approves with fixed loan terms.
    """
    return Response(
        result="1",
        score=score,
        strategy_name="pure_stream_strategy",
        loan_amount=8000,
        loan_term=6,
        created_at=datetime.now()
    )


def apply_new_client(score: float) -> Response:
    """
    New Client Strategy:
    - Approves if score < 0.15
    - Offers 6000 over 3 months
    """
    result = "1" if score < 0.15 else "0"
    return Response(
        result=result,
        score=score,
        strategy_name="new_client_strategy",
        loan_amount=6000 if result == "1" else None,
        loan_term=3 if result == "1" else None,
        created_at=datetime.now()
    )


def apply_repeat_client(score: float, phone: str) -> Response:
    """
    Repeat Client Strategy:
    - Pilot strategy if phone ends with 2 or 4
    - Regular strategy otherwise
    """
    if phone[-1] in {"2", "4"}:
        result = "1" if score < 0.18 else "0"
        return Response(
            result=result,
            score=score,
            strategy_name="pilot_repeat_client_strategy",
            loan_amount=24000 if result == "1" else None,
            loan_term=12 if result == "1" else None,
            created_at=datetime.now()
        )
    else:
        result = "1" if score < 0.20 else "0"
        return Response(
            result=result,
            score=score,
            strategy_name="repeat_client_strategy",
            loan_amount=12000 if result == "1" else None,
            loan_term=6 if result == "1" else None,
            created_at=datetime.now()
        )


# ========== MAIN ENTRYPOINT ==========

def main(request: Request) -> Response:
    """
    Main decision function. Applies strategy based on client type and rules.
    """
    try:
        base_path = request.context

        # Load Application.json
        app_path = base_path / "Application" / "Application.json"
        app_data = json.loads(app_path.read_text())
        client_type = app_data["client_type"]

        # Load SqlIntegration.json
        sql_path = base_path / "SqlIntegration" / "SqlIntegration.json"
        sql_data = json.loads(sql_path.read_text())
        phone = sql_data["phone_number"]

        # Load scoring file dynamically (supports versioning)
        scoring_dir = next((f for f in os.listdir(base_path) if f.startswith("PythonScoring")), None)
        if scoring_dir is None:
            raise FileNotFoundError("Scoring directory not found")

        scoring_files = os.listdir(base_path / scoring_dir)
        scoring_file = next((f for f in scoring_files if f.endswith(".json")), None)
        if scoring_file is None:
            raise FileNotFoundError("Scoring file not found inside scoring directory")

        scoring_path = base_path / scoring_dir / scoring_file
        scoring_data = json.loads(scoring_path.read_text())
        score = scoring_data["score"]

        # Strategy selection
        if is_pure_stream(request.request_id):
            return apply_pure_stream(score)

        if client_type == "new":
            return apply_new_client(score)
        elif client_type == "repeat":
            return apply_repeat_client(score, phone)

        # Handle unexpected client types
        return Response(
            result="error",
            score=score,
            strategy_name="unknown_client_type",
            loan_amount=None,
            loan_term=None,
            created_at=datetime.now()
        )

    except Exception as e:
        # Log and return error response
        print(f"[ERROR] Failed to process request_id={request.request_id} → {e}")
        return Response(
            result="error",
            score=-1.0,
            strategy_name="error",
            loan_amount=None,
            loan_term=None,
            created_at=datetime.now()
        )
