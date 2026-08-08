from studio.storyboard.shot_sequence import ShotSequence


class ShotPlanner:
    def order(self, sequence: ShotSequence) -> ShotSequence:
        sequence.shots = sequence.ordered_shots()
        return sequence
