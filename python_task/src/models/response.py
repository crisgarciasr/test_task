from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Literal, Optional


@dataclass
class Response:
    result: Literal["1", "0", "error"] = field(default="0")
    score: float = field(default=-999)
    strategy_name: str = field(default="")
    loan_term: Optional[int] = field(default=None)
    loan_amount: Optional[float] = field(default=None)

    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result": self.result,
            "score": self.score,
            "strategy_name": self.strategy_name,
            "created_at": datetime.strftime(self.created_at, "%Y-%m-%d %H:%M:%S"),
        }
