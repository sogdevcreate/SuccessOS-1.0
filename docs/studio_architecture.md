# SuccessOS AI Film Studio architecture

## Package structure

`studio.models` contains the serializable production aggregate, the film-wide `ProductionProfile`, the `DirectorsBible`, and typed production artifacts. `studio.enums` defines project, quality, media, asset, pipeline, and per-stage state. `studio.interfaces` contains provider-facing abstract contracts. `studio.services` owns persistence, versioning, quality evaluation, and pipeline state transitions. `studio.pipeline` coordinates injected stage executors.

## StudioProject data flow

`StudioProject` is the single source of truth for one film production. Every project owns exactly one `ProductionProfile` and one `DirectorsBible`. A stage executor receives a `PipelineContext` containing that project and exposes both creative artifacts as typed context properties. It reports the outcome through a typed `StageResult`. Executors do not receive, or mutate, another executor's separate domain object. The pipeline persists the aggregate after state transitions and captures a version after each successful stage.

The research stage stores a typed `ResearchReport` on the same aggregate. It keeps source acquisition outside the Studio pipeline while providing evidence validation, ranking, contradiction handling, cinematic research opportunities, and a dedicated quality review before Script can proceed.

The Script stage stores a typed `Screenplay` on the aggregate and treats `ResearchReport` as read-only evidence. It validates scene-level fact traceability, unsupported claims, disputed claims, continuity, ProductionProfile alignment, and Director's Bible constraints before the screenplay quality gate permits Storyboard.

The Storyboard stage stores `CinematicStoryboard`, a photorealistic-cinematic shot plan that keeps the screenplay read-only. It validates scene traceability, professional camera/lens/lighting plans, visual continuity, and 180-degree-rule metadata before gating Characters, Scene Planning, and Assets.

The Character/Environment Continuity stage stores typed identity, wardrobe, environment, prop, and snapshot data in `ContinuityRegistry`. Its visual identity locks are provider-neutral inputs for future generation engines, while screenplay and storyboard remain read-only. It gates Scene Planning; Assets additionally require completed Scene Planning.

Scene Planning stores provider-neutral `ScenePlan` and `AssetSpecification` records. These bind the approved screenplay, storyboard, and continuity state into explicit photorealistic production instructions; future providers must consume specifications and generation instructions rather than bypass them.

Asset Generation stores provider-ready requests, jobs, manifests, generated-asset provenance, and quality decisions. It selects only registered providers that satisfy hard specifications, never claims media exists without a provider result, and gates Animation on accepted assets.

Animation stores provider-neutral shot requests, performance plans, temporal continuity, jobs, assemblies, and quality decisions. It uses approved assets as read-only input and gates Voice/Music on accepted animated shots.

Audio Production models voice acting, score, sound design, timelines, and mixes as provider-neutral production state. It gates Video Editing on approved voice and music/sound stages.

## Film direction

`ProductionProfile` expresses the production's target platform, genre, realism level, visual and rendering styles, camera, lighting, color, motion, voice, music, audience, duration, and language. `DirectorsBible` holds the story vision and rules for visuals, characters, camera, lighting, pacing, editing, emotion, quality, and continuity. Both are serialized and versioned with the project, so all stages operate against the same creative direction.

## Pipeline lifecycle

The fixed order is Idea, Research, Script, Storyboard, Characters, Scene Planning, Assets, Animation, Voice, Music/SFX, Video Edit, Thumbnail, Metadata/SEO, Publish, and Analytics. The pipeline can start at a selected stage, pause, resume, cancel, retry the failed stage, or mark a documented optional stage as skipped. It requires an explicitly registered executor; an unregistered stage fails rather than claiming production work occurred. A supplied quality report must pass before the pipeline advances. Script requires Research, Storyboard requires Script, Characters requires Storyboard, Scene Planning requires approved Character/Environment Continuity, and Assets requires all three upstream stages plus Scene Planning—even for direct-resume attempts.

## Versioning

`VersionManager` creates immutable-by-copy snapshots of the aggregate payload. It lists snapshots, compares their changed top-level fields, restores a selected snapshot, and rolls back to the most recent snapshot. Restoring preserves the timeline so a production retains its version history.

## Quality system

Each `QualityScore` has a 0.0–10.0 score and a non-negative weight. `QualityReport` computes a weighted overall score, evaluates a configured threshold, records reviewer comments and improvement suggestions, and tracks regeneration attempts. Reaching the configured retry limit without passing produces `retry_exhausted`.

## Creator, Reviewer, Director

Creator-facing interfaces produce typed stage results. A `Reviewer` returns a `QualityReport`, which gates progression. A `Director` exposes an explicit approval contract. This makes the human or provider roles composable without coupling a provider to Studio persistence or another provider's artifact model.

## Future extensions

Implement an interface for an AI, image, video, audio, publishing, or analytics provider and register a small adapter as the relevant pipeline executor. The adapter receives the shared project, `ProductionProfile`, and `DirectorsBible` through `PipelineContext`; it may update `StudioProject` only for its own stage's resulting domain fields and must return an honest `StageResult`. Repository implementations may be replaced with a durable database repository while retaining `ProjectRepository`, `VersionManager`, and `StudioPipeline` construction boundaries.
