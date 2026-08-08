from studio.storyboard.lighting_plan import LightingPlan


class LightingDirector:
    def validate(self, plan: LightingPlan) -> list[str]:
        return [] if plan.mood or plan.key_light else ["Lighting plan requires a key light or mood"]
