from studio.storyboard.composition_plan import CompositionPlan


class CompositionAnalyzer:
    def validate(self, composition: CompositionPlan) -> list[str]:
        return [] if composition.framing and composition.camera_angle else ["Composition requires framing and camera angle"]
