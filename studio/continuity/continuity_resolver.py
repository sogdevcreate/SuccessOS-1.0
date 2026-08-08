from studio.continuity.continuity_registry import ContinuityRegistry
from studio.continuity.continuity_snapshot import ContinuitySnapshot


class ContinuityResolver:
    def restore(self, registry: ContinuityRegistry, snapshot: ContinuitySnapshot) -> None: registry.restore(snapshot)
