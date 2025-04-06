import json
from python_task.src.models import Request, Response
from random import choice


def main(request: Request) -> Response:
    # Example of how to read the data from the request
    application_data_path = request.context / "Application" / "Application.json"
    application_data = json.loads(application_data_path.read_text())

    # TODO: Implement your scoring logic here

    # Example of returning a response
    return Response(
        strategy_name=choice(["strategy_1", "strategy_2", "strategy_3"]),
        result="0",
        score=-999,
        loan_amount=10_000,
        loan_term=6,
    )
