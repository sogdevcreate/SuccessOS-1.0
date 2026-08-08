from studio.continuity.continuity_registry import ContinuityRegistry


class ContinuityValidator:
    def validate(self, registry: ContinuityRegistry) -> list[str]:
        errors: list[str] = []
        for character in registry.characters.values():
            if not character.visual_identity_lock.locked_appearance_attributes:
                errors.append(f"Character '{character.unique_id}' has no visual identity lock")
            costume_ids = [costume.costume_id for costume in character.wardrobe]
            if len(costume_ids) != len(set(costume_ids)):
                errors.append(f"Character '{character.unique_id}' has duplicate costume identifiers")
        for prop in registry.props.values():
            if not prop.current_location:
                errors.append(f"Prop '{prop.identity}' has no current location")
        for environment in registry.environments.values():
            if not environment.time_of_day or not environment.weather:
                errors.append(f"Environment '{environment.identity}' lacks time-of-day or weather continuity")
        return errors

    def detect_drift(self, previous, current) -> list[str]:
        errors: list[str] = []
        for identifier, state in current.character_states.items():
            if identifier in previous.character_states and state.get("age_state") != previous.character_states[identifier].get("age_state"):
                errors.append(f"Character appearance drift: {identifier}")
        for identifier, state in current.prop_states.items():
            prior = previous.prop_states.get(identifier)
            if prior and state.get("location") != prior.get("location") and not state.get("location"):
                errors.append(f"Prop teleportation: {identifier}")
            if prior and state.get("damage") != prior.get("damage") and not state.get("damage"):
                errors.append(f"Unexplained damage change: {identifier}")
        for identifier, state in current.environment_states.items():
            prior = previous.environment_states.get(identifier)
            if prior and state.get("time_of_day") != prior.get("time_of_day") and not current.time_progression:
                errors.append(f"Time-of-day conflict: {identifier}")
            if prior and state.get("weather") != prior.get("weather") and not current.time_progression:
                errors.append(f"Weather conflict: {identifier}")
        return errors
