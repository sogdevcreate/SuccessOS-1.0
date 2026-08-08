# SuccessOS AI YouTube Studio architecture

## Package structure

`studio.models` contains the serializable production aggregate and its typed artifacts. `studio.enums` defines project, quality, media, asset, pipeline, and per-stage state. `studio.interfaces` contains provider-facing abstract contracts. `studio.services` owns persistence, versioning, quality evaluation, and pipeline state transitions. `studio.pipeline` coordinates injected stage executors.

## StudioProject data flow

`StudioProject` is the single source of truth for one production. A stage executor receives a `PipelineContext` containing that project and reports the outcome through a typed `StageResult`. Executors do not receive, or mutate, another executor's separate domain object. The pipeline persists the aggregate after state transitions and captures a version after each successful stage.

## Pipeline lifecycle

The fixed order is Idea, Research, Script, Storyboard, Characters, Scene Planning, Assets, Animation, Voice, Music/SFX, Video Edit, Thumbnail, Metadata/SEO, Publish, and Analytics. The pipeline can start at a selected stage, pause, resume, cancel, retry the failed stage, or mark a documented optional stage as skipped. It requires an explicitly registered executor; an unregistered stage fails rather than claiming production work occurred. A supplied quality report must pass before the pipeline advances.

## Versioning

`VersionManager` creates immutable-by-copy snapshots of the aggregate payload. It lists snapshots, compares their changed top-level fields, restores a selected snapshot, and rolls back to the most recent snapshot. Restoring preserves the timeline so a production retains its version history.

## Quality system

Each `QualityScore` has a 0.0–10.0 score and a non-negative weight. `QualityReport` computes a weighted overall score, evaluates a configured threshold, records reviewer comments and improvement suggestions, and tracks regeneration attempts. Reaching the configured retry limit without passing produces `retry_exhausted`.

## Creator, Reviewer, Director

Creator-facing interfaces produce typed stage results. A `Reviewer` returns a `QualityReport`, which gates progression. A `Director` exposes an explicit approval contract. This makes the human or provider roles composable without coupling a provider to Studio persistence or another provider's artifact model.

## Future extensions

Implement an interface for an AI, image, video, audio, publishing, or analytics provider and register a small adapter as the relevant pipeline executor. The adapter may update the shared `StudioProject` only for its own stage's resulting domain fields and must return an honest `StageResult`. Repository implementations may be replaced with a durable database repository while retaining `ProjectRepository`, `VersionManager`, and `StudioPipeline` construction boundaries.
