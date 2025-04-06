from collections import Counter
import json
from pathlib import Path

from rich import print


def strategies_counters():
    strategies: Counter[str] = Counter()

    test_result_folder = Path(__file__).parent / "test_result"
    if not test_result_folder.exists():
        print("[bold red]No test results found.")
        print("Please generate the dummy data and run the tests first.")
        print("See the README for more details.")
        return

    for result_file in test_result_folder.iterdir():
        if not result_file.is_file():
            continue
        if result_file.suffix != ".json":
            continue
        result = json.loads(result_file.read_text())
        strategy = result.get("strategy_name", "unknown")
        strategies[strategy] += 1

    print("Strategies counters:")
    print(strategies)


if __name__ == "__main__":
    strategies_counters()
