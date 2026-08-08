from dataclasses import dataclass
@dataclass(frozen=True)
class ProviderScore:
    provider_id: str; score: float; reasons: tuple[str, ...] = ()
