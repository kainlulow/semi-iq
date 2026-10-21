# SemiIQ V1.0.0 — Release Notes

## Overview

This V1.0.0 publication package comprises **225 human-approved WP1 knowledge records** and **769 human-approved WP2 assessment items**, with **1,247 scoring criteria** covering six semiconductor knowledge modules. The public dataset preserves the approved technical content while excluding private workflow fields and source-mirror process annotations. JSON is authoritative, with an exactly corresponding XLSX projection for browsing and response entry.

## Public licenses

- Original authored WP1/WP2 data and documentation: **CC BY-NC 4.0**.
- Original software, scripts, examples and authored CI workflows: **PolyForm Noncommercial 1.0.0**.
- Additional commercial rights: **separate negotiated agreement with the relevant authorized rights holder(s)**.
- Release owner and licensing representative: **Kain Lu Low, acting on behalf of the authorized licensors**.

See `LICENSE`, `LICENSING.md` and `COMMERCIAL-LICENSING.md`. These are **non-commercial source-available** terms; they are not OSI-approved open-source terms.

## Verification

Run `python scripts/validate_release.py` to check cross-links, scoring totals, privacy rules, exact XLSX–JSON correspondence and checksums. Technical-source citations are retained; external source PDFs are not distributed.

## Responsible evaluation

The benchmark is public and contains reference answers and scoring criteria. For model evaluation, only `item.question`, `item.input_data`, and `item.assumptions` should be model-facing. Keep reference answers/rubrics outside prompts and retrieval contexts; avoid presenting public items as unseen hold-out tests.

## Source traceability

The source register and item-level source index provide deterministic citation-string keys while retaining legacy module-local `SRC-###` aliases. Source-reference/locator named-work consistency was checked against the cited Pierret and Taur–Ning editions at item level, with locators identifying relevant chapters, sections and physical PDF pages. These metadata checks improve traceability but do not replace independent scientific interpretation of every claim.

## Publication information

Version: `v1.0.0` (proposed GitHub tag). This package does not itself imply that a GitHub repository or release has already been created. Public publication date, DOI and repository URL should be filled in once assigned, without guessing them in metadata. Required publication rights are reported obtained by the release owner; documentary evidence is not part of the repository.

## Public schema simplification

The V1.0.0 public distribution excludes per-record contributor/reviewer/status metadata, generator-stage statuses, warning placeholders, redundant versions and local PDF-mirror hashes. Source locators and scoring evidence retain their technical content.

## WP2 release contents

The public WP2 dataset contains **570 conceptual-rubric, 146 exact-answer and 53 numeric-with-tolerance items**. The release validator checks score totals and targeted task–criterion alignments; it does not establish universal semantic agreement between prose rubrics, reference answers and criteria.

The public schema excludes private review fields and evidence-binding workflow metadata. GitHub Actions must still be checked after publication.
