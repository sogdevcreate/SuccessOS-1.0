# Screenwriting Engine

## Purpose

The AI Film Studio Screenwriting Engine turns a supplied, verified `ResearchReport` and a supplied typed `Screenplay` into a validated, quality-reviewed Script-stage artifact. It does not generate prose, scenes, or dialogue. Future LLM adapters implement `ScreenplayProvider` and return a typed `Screenplay` for this engine to validate.

## Data boundaries

The engine reads `ResearchReport`, `ProductionProfile`, and `DirectorsBible` through `PipelineContext`. Research is treated as read-only. The only project field it may replace is `StudioProject.screenplay`, after deterministic normalization and validation. It produces an honest failed `StageResult` when research or a screenplay is absent or invalid.

## Screenplay model

`Screenplay` holds the title, logline, premise, genre, tone, audience, hook, opening sequence, act and sequence structure, ordered scenes, character and emotional arcs, pacing notes, tension curve, callbacks, reveals, climax, resolution, call to action, and calculated runtime.

Each `ScreenplayScene` retains its id, number, slugline, location, time of day, duration, participants, dramatic/visual/emotional objectives, action, dialogue, narration, transitions, source and fact references, unsupported claims, disputed-fact references, continuity requirements, Director's Bible constraints, and ordered beats.

## Factual integrity

`ScreenplayValidator` validates every fact reference against the report. A scene that uses a disputed report fact must list it in `disputed_fact_references`; it cannot silently present the claim as verified. Unknown factual references are rejected. Unsupported content is an explicit scene or beat field, never inferred as verified evidence.

## Quality gate

`ScreenplayQualityReviewer` evaluates hook, storytelling, structure, pacing, emotional engagement, dialogue, narration, character consistency, factual fidelity, cinematic potential, audience retention, ProductionProfile compliance, and Director's Bible compliance. The project quality threshold determines pass/fail. Storyboard has an explicit prerequisite on a successfully completed Script stage, including direct-resume attempts.

## Extension model

Future LLM implementations live behind `ScreenplayProvider.create(research_report, profile, bible)`. They remain separate from validation, quality review, persistence, versioning, and stage control, so multiple providers can be composed without weakening factual or pipeline guarantees.
