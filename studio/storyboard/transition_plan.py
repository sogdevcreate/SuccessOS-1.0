from dataclasses import dataclass


@dataclass
class TransitionPlan:
    transition_in: str = "cut"
    transition_out: str = "cut"

    def to_dict(self) -> dict[str, object]:
        return {"transition_in": self.transition_in, "transition_out": self.transition_out}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "TransitionPlan":
        return cls(**data)
