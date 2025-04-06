from abc import ABC, abstractmethod
import json
from pathlib import Path
from random import choice, choices, normalvariate, randint
from typing import Any, Dict
from uuid import uuid4
from rich import print

from faker import Faker

fake = Faker()

project_dir = Path(__file__).resolve().parent

DUMMY_FOLDERS_CNT = 100


class FakeDataGenerator(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    def dump(self, path: Path) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.to_dict()})"


class FakeRequest(FakeDataGenerator):
    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "client_type": self.client_type,
        }

    def __init__(self):
        self.request_id = str(uuid4())
        self.client_type = choices(("new", "repeat"), weights=(0.4, 0.6), k=1)[0]


class FakeSqlIntegration(FakeDataGenerator):
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "age": self.age,
            "sex": self.sex,
            "document_id": self.document_id,
            "address": self.address,
            "phone_number": self.phone,
        }

    def __init__(self):
        self.name = fake.name()
        self.age = randint(21, 60)
        self.sex = choice(("Male", "Female"))
        self.document_id = fake.random_number()
        self.address = fake.address()
        self.phone = fake.phone_number()


class FakePythonScoring(FakeDataGenerator):
    def to_dict(self) -> Dict[str, Any]:
        return {"score": self.score}

    def __init__(self):
        self.score = abs(normalvariate(0.2, 0.1))


def delete_folder(path: Path):
    for sub in path.iterdir():
        if sub.is_dir():
            delete_folder(sub)
        else:
            if sub.suffix == ".json":
                sub.unlink()
            else:
                raise ValueError(f"Careful! Unknown file type: {sub.suffix}, it should be .json")
    path.rmdir()


def main():
    test_data_dir = project_dir / "test_data"
    if test_data_dir.exists():
        delete_folder(test_data_dir)
    test_data_dir.mkdir()

    for _ in range(DUMMY_FOLDERS_CNT):
        request = FakeRequest()
        sql_integration = FakeSqlIntegration()
        python_scoring = FakePythonScoring()

        decision_dir = test_data_dir / request.request_id
        decision_dir.mkdir(exist_ok=True)

        request_dir = decision_dir / "Application"
        request_dir.mkdir(exist_ok=True)
        request.dump(request_dir / "Application.json")

        sql_integration_dir = decision_dir / "SqlIntegration"
        sql_integration_dir.mkdir(exist_ok=True)
        sql_integration.dump(sql_integration_dir / "SqlIntegration.json")

        random_version = randint(1, 3)
        python_scoring_dir = decision_dir / f"PythonScoring-v{random_version}"
        python_scoring_dir.mkdir(exist_ok=True)
        python_scoring.dump(python_scoring_dir / f"PythonScoring-v{random_version}.json")

    print("[bold green]Fake data generated successfully!:rocket-emoji:")


if __name__ == "__main__":
    main()
