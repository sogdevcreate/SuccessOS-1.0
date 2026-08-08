class HookGenerator:
    """Validates supplied hooks; future LLM providers may supply hook candidates."""

    def normalize(self, hook: str) -> str:
        return hook.strip()
