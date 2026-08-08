class GenerationValidator:
    def validate(self, request):
        errors=[]
        if not request.asset_specification.identity_locks: errors.append("Generation request lacks identity-lock bindings")
        if not request.asset_specification.generation_instruction.modalities: errors.append("Generation request lacks generation modality")
        return errors
