from studio.screenwriting.screenplay import Screenplay


class ContinuityChecker:
    def check(self, screenplay: Screenplay) -> list[str]:
        issues: list[str] = []
        seen_numbers: set[int] = set()
        for scene in screenplay.scenes:
            if scene.scene_number in seen_numbers:
                issues.append(f"Duplicate scene number: {scene.scene_number}")
            seen_numbers.add(scene.scene_number)
            if not scene.directors_bible_constraints:
                issues.append(f"Scene '{scene.id}' has no Director's Bible constraints")
        return issues
