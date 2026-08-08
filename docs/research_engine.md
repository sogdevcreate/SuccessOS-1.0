# Research Engine

## Purpose

The AI Film Studio Research Engine turns an already acquired, typed body of evidence into a structured `ResearchReport` for cinematic development. It never fetches sources, invents facts, or reports research success when no evidence package exists.

## Boundaries and flow

Future web, search, archive, or API adapters implement `ResearchSourceProvider.acquire(topic)` and return typed `ResearchSource` records. Source acquisition is intentionally separate from analysis. The provider-neutral `ResearchPipeline` then normalizes supplied questions, facts, and entities; ranks sources; orders the timeline; detects supported contradiction relationships; extracts lexical keywords; and validates all references.

`ResearchEngine` is the StudioPipeline adapter. It receives `PipelineContext`, so the shared `ProductionProfile` and `DirectorsBible` remain available for every implementation. It requires the project to contain a `ResearchReport`, analyzes that evidence, stores the report back into the same `StudioProject`, and returns a typed stage result with a research quality report.

## Evidence model

Each source retains its identity, bibliographic data, source type, dates, reliability and relevance scores, bias/risk notes, and citation metadata. Facts record source references, confidence (0.0–1.0), verification state, dispute state, and contradiction references. Citations point to sources and optional locators. Entities and timeline events retain source references and confidence.

`ResearchReport` contains the topic, questions, executive summary, fact sets, unresolved questions, chronology, entities and typed views of people/organizations/locations/dates, terminology, keywords, themes, sources, citations, contradictions, confidence scores, visual and archive needs, scene and script ideas, hooks, thumbnails, and legal-risk notes.

## Quality gate

`ResearchQualityReviewer` scores factual reliability, source diversity, source quality, completeness, contradiction handling, citation coverage, storytelling usefulness, and visual usefulness from 0.0–10.0. The result uses the project quality threshold. `StudioPipeline` cannot run Script unless Research is marked successful, which only happens after that gate passes.

## Extension model

Add source-acquisition adapters behind `ResearchSourceProvider`; do not combine them with ranking, verification, or quality review. New providers can be composed before `ResearchPipeline` without changing Studio project persistence, quality gating, or the pipeline contract.
