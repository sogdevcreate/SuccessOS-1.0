from studio.screenwriting.dialogue_line import DialogueLine


class DialoguePlanner:
    def normalize(self, lines: list[DialogueLine]) -> list[DialogueLine]:
        return [line for line in lines if line.character.strip() and line.text.strip()]
