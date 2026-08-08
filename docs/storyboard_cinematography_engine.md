# Storyboard and Cinematography Engine

## Purpose

The Storyboard Engine turns a supplied approved `Screenplay` and a supplied `CinematicStoryboard` into a validated visual plan. It does not generate images, video, or rendered assets. Future planning providers implement `StoryboardProvider`; rendering providers remain outside this package.

## Cinematic visual model

`CinematicStoryboard` defaults to the design target `cinematic photorealism`. It contains storyboard scenes, each bound to a screenplay scene and an ordered shot sequence. A shot includes its id, screenplay scene and sequence references, shot number/type, composition, camera plan, blocking, environment and prop requirements, lighting plan, duration, transitions, dialogue/narration timing, effects needs, continuity metadata, and screenplay references.

Camera plans represent position, target, movement, lens/focal length, depth of field, stabilization, speed, timing, and focus transitions. Supported professional movements include tracking, dolly, crane, handheld, steadicam, orbit, rack focus, push-in, pull-out, pan, and tilt. Lighting plans describe key/fill/rim lights, practicals, environment/time-of-day light, exposure, contrast, shadow, temperature, and mood.

## Continuity and traceability

Every storyboard scene and shot must resolve to a screenplay scene. Visual continuity tracks character, location, costume, prop, lighting, screen direction, and axis-of-action requirements. The checker reports inconsistent protected 180-degree-rule axes inside a storyboard scene. The storyboard only writes `StudioProject.cinematic_storyboard`; the screenplay stays read-only.

## Quality and pipeline gates

The reviewer scores composition, variety, motivation, camera and lighting continuity, visual/emotional storytelling, pacing, character/environment continuity, screenplay fidelity, profile and Bible compliance, and photorealistic feasibility. After Storyboard passes the project quality threshold, its version is snapshotted. Characters, Scene Planning, and Assets each require a passed Storyboard stage, even when resumed directly.

## Extension model

Provider implementations may create typed `CinematicStoryboard` instances from an approved screenplay and the shared production direction. They cannot claim rendered output, bypass validation, mutate screenplay data, or replace the pipeline quality gate.
