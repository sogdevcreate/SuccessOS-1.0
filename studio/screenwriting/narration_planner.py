from studio.screenwriting.narration_block import NarrationBlock


class NarrationPlanner:
    def normalize(self, blocks: list[NarrationBlock]) -> list[NarrationBlock]:
        return [block for block in blocks if block.text.strip()]
