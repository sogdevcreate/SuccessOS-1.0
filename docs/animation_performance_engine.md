# Animation and Performance Engine

The Animation subsystem is provider-neutral orchestration for approved generated assets. It stores typed motion, facial performance, lip-sync, camera motion, reference, temporal/frame continuity, requests, jobs, assemblies, and shot provenance. It has no external provider or fake completed clip path.

Future providers implement the animation provider contract and declare video, motion, facial, lip-sync, camera, frame, duration, resolution, fps, and aspect-ratio capabilities. The selector rejects providers that cannot satisfy hard request requirements. Missing providers leave a real unavailable state.

Assets must be approved before animation. Animated shots must pass the project quality threshold before Voice or Music/SFX may advance. Provenance includes source assets, storyboard/shot, provider, timing, seed/reference metadata, quality decisions, regeneration state, and continuity handoff.
