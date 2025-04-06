import json
from pathlib import Path

from tqdm import tqdm

from python_task.src.models import Request, Response
from python_task.scoring import main


def run() -> None:
    test_data_dir = Path(__file__).parent / "test_data"
    test_result_dir = Path(__file__).parent / "test_result"

    if not test_data_dir.exists():
        return

    test_result_dir.mkdir(exist_ok=True)

    for sub_dir in tqdm(list(test_data_dir.iterdir())):
        if not sub_dir.is_dir():
            continue
        request_id = sub_dir.name
        request = Request(request_id=request_id, context=sub_dir)
        response: Response = main(request)

        result_file_path = test_result_dir / f"{request_id}.json"
        with open(result_file_path, "w") as f:
            f.write(json.dumps(response.to_dict(), indent=4))


if __name__ == "__main__":
    run()
