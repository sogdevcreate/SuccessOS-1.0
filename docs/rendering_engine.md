# Rendering Engine

The Rendering Engine is provider-neutral. It validates approved edit/color inputs, render/export profiles, logical source media, output destination, and provider capabilities before submission. Missing compatible providers produce an explicit unavailable result; no master file is fabricated.

`RenderProfile` captures video, audio, color, HDR/SDR, subtitle, and quality settings. `FinalFilmManifest` preserves production versions, sources, edit/color/render provenance, providers, quality, and rights metadata. Publishing requires approved Rendering through the explicit pipeline stage.
