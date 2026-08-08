from studio.storyboard.storyboard import CinematicStoryboard


class ContinuityChecker:
    def check(self, storyboard: CinematicStoryboard) -> list[str]:
        issues: list[str] = []
        for scene in storyboard.scenes:
            axes = {shot.continuity.axis_of_action for shot in scene.sequence.shots if shot.continuity.preserve_180_degree_rule and shot.continuity.axis_of_action}
            if len(axes) > 1:
                issues.append(f"Storyboard scene '{scene.screenplay_scene_id}' violates the 180-degree rule")
        return issues
