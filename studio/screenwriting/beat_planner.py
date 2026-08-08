from studio.screenwriting.screenplay_beat import ScreenplayBeat


class BeatPlanner:
    def order(self, beats: list[ScreenplayBeat]) -> list[ScreenplayBeat]:
        return sorted(beats, key=lambda beat: beat.sequence)
