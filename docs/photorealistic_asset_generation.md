# Photorealistic Asset Generation Architecture

The generation subsystem is provider-neutral orchestration, not a media provider. It turns approved `AssetSpecification` records into `GenerationRequest`s, validates hard capability constraints, selects an enabled healthy provider, creates dependency-aware jobs, records provenance, and quality-gates generated artifacts.

`GenerationProvider` is the future provider contract: availability, request validation, estimates, submission, status, result, and cancellation. `GenerationProviderRegistry` stores enabled/health/priority/cost/quality metadata. `ProviderSelector` rejects providers that cannot satisfy specification modalities, conditioning, aspect ratio, or duration constraints.

`GeneratedAsset` preserves specification, provider job, request, timestamps, resolution, seed, model/version, reference and identity bindings, continuity snapshot, quality, acceptance, regeneration, metadata, and provenance. No provider configured or no generated artifact available is an explicit failure state.

The Asset stage accepts only artifacts whose quality report meets the project threshold. Animation requires the Asset stage to have passed. Future providers must consume `AssetSpecification` and `GenerationInstruction`, including reference conditioning for identity, wardrobe, pose, depth, masks, environment, style, camera, and prior frames.
