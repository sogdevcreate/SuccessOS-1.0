from studio.screenwriting.story_structure import StoryStructure


class OutlineBuilder:
    def normalize(self, structure: StoryStructure) -> StoryStructure:
        structure.acts = [act.strip() for act in structure.acts if act.strip()]
        structure.sequences = [sequence.strip() for sequence in structure.sequences if sequence.strip()]
        return structure
