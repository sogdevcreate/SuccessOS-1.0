from studio.research.entity import Entity


class EntityExtractor:
    def normalize(self, entities: list[Entity]) -> list[Entity]:
        unique: dict[tuple[str, str], Entity] = {}
        for entity in entities:
            key = (entity.name.casefold(), entity.entity_type.value)
            unique.setdefault(key, entity)
        return list(unique.values())
