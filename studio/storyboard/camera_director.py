from studio.storyboard.camera_plan import CameraPlan


class CameraDirector:
    SUPPORTED_MOVEMENTS = frozenset({"tracking", "dolly", "crane", "handheld", "steadicam", "orbit", "rack focus", "push-in", "pull-out", "pan", "tilt"})

    def validate(self, plan: CameraPlan) -> list[str]:
        return [] if not plan.movement_path or plan.movement_path in self.SUPPORTED_MOVEMENTS else [f"Unsupported camera movement: {plan.movement_path}"]
