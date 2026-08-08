from dataclasses import dataclass

@dataclass(frozen=True)
class PerformanceMetric:
    name: str
    value: float | int | None
    unit: str = ""
    source: str = ""
    observed_at: str = ""
    provenance: dict[str, str] | None = None
    def to_dict(self): return {"name": self.name, "value": self.value, "unit": self.unit, "source": self.source, "observed_at": self.observed_at, "provenance": dict(self.provenance or {})}
    @classmethod
    def from_dict(cls, data): return cls(str(data["name"]), data.get("value"), str(data.get("unit", "")), str(data.get("source", "")), str(data.get("observed_at", "")), dict(data.get("provenance", {})))
