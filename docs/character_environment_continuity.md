# Character, Environment, and Continuity Engine

## Purpose

This provider-neutral engine preserves photorealistic cinematic identity and world state across a production. It never generates images, video, or assets. Its inputs are the read-only storyboard and screenplay plus the project-wide production direction; it writes only continuity-domain state held in `StudioProject` and `ContinuityRegistry`.

## Identity and world state

`CharacterProfile` combines stable identity, facial/body constraints, mannerisms, wardrobe, accessories, injury/age/emotional state, voice identity, and `VisualIdentityLock`. The lock holds reference asset IDs and handles, seed metadata, prompt anchors, negative constraints, locked attributes, and provider metadata for future image/video providers.

`EnvironmentProfile` records location, geography, architecture, set layout, period, weather, season, time, lighting, materials, palette, furnishings, vehicles, recurring props, damage, and history. `PropProfile` tracks ownership, location, use, damage, and history. The default design target is cinematic photorealism; no anime/cartoon-specific behavior is introduced.

## Registry and validation

`ContinuityRegistry` is the central record of characters, environments, props, and scene snapshots. It creates and restores `ContinuitySnapshot` state for age/injury, object ownership/location/damage, environment time/weather/damage, and time progression. Validation detects missing visual locks, duplicate costumes, missing prop location, and incomplete environment state. Snapshot comparison detects appearance drift, unexplained damage changes, time-of-day conflicts, and weather conflicts.

## Quality and pipeline

Character and environment reviewers score their required criteria from 0.0–10.0. The combined Character/Environment Continuity executor runs at the existing `CHARACTERS` stage and requires an approved cinematic storyboard. Its quality report must meet the project threshold before Scene Planning. Assets require approved Storyboard, approved continuity, and completed Scene Planning. Successful continuity stages receive the standard project version snapshot and can use existing restore/rollback support.

## Extension model

Future image or video generators must consume `VisualIdentityLock` and `ContinuityRegistry` when they are introduced. Provider adapters may supply typed profile data, but cannot fabricate assets, mutate screenplay/storyboard, bypass validation, or claim a successful generation stage.
