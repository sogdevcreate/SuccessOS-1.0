from studio.screenwriting.screenplay import Screenplay


class PacingAnalyzer:
    def analyze(self, screenplay: Screenplay) -> list[float]:
        """Returns a scene-order tension curve using declared beat tension only."""
        curve: list[float] = []
        for scene in screenplay.ordered_scenes():
            tensions = [beat.tension for beat in scene.beats]
            curve.append(sum(tensions) / len(tensions) if tensions else 0.0)
        return curve
