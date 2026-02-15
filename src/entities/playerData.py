from dataclasses import dataclass, field
from typing import List
from .fairy import Fairy
from .unicorn import Unicorn

@dataclass
class PlayerData:
    level: int = 1
    currency: int = 500
    reputation: int = 0
    decision_history: List[str] = field(default_factory=list)
    unicorns: List[Unicorn] = field(default_factory=list)
    fairies: List[Fairy] = field(default_factory=list)

    def can_afford(self, amount: int) -> bool:
        return self.currency >= amount