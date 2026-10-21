# SemiIQ

**Version:** V1.0.0 · **Data:** 225 approved WP1 knowledge records and 769 approved WP2 assessment items · **Distribution:** validated GitHub publication package (remote CI pending).

SemiIQ provides a structured semiconductor science and engineering knowledge and AI-evaluation benchmark spanning six fixed modules. WP1 contains approved knowledge records. WP2 supplies questions, task inputs, assumptions, reference answers, scoring criteria, technical-source citations, and exact WP1 links.

This V1.0.0 distribution contains the approved WP1 knowledge collection and WP2 assessment collection, with private workflow metadata and local source-file fingerprints excluded from the public schema. The release owner has confirmed that required publication permissions were obtained; signed documentation remains private. See [LICENSING.md](LICENSING.md) for the exact non-commercial license scope.

## Dataset coverage

| Module | Abbreviation | WP2 questions |
|---|---|---:|
| Semiconductor Fundamentals | SEM | 120 |
| Device Physics | DEV | 180 |
| Material Properties | MAT | 102 |
| Process Physics | PRO | 142 |
| Modeling and Simulation | SIM | 108 |
| Engineering Applications | ENG | 117 |
| **Total** | | **769** |

Difficulty: Basic **232**, Intermediate **369**, Advanced **168**. The dataset contains **1,247** scoring criteria across exact-answer, numeric-tolerance, and conceptual-rubric tasks.

## Contents

- `data/v1.0/wp1_knowledge.json` — authoritative WP1 knowledge records.
- `data/v1.0/wp2_benchmark.json` — authoritative WP2 assessment data and scoring metadata.
- `data/v1.0/wp2_benchmark.xlsx` — browsing and response-entry workbook; JSON retains the complete scoring policy.
- `metadata/source_register.csv` — unique source-**string** keys, citation text, usage counts and bibliographic display.
- `metadata/source_item_index.csv` — per-record mapping to those unique keys, including legacy module-local source aliases.
- `metadata/content_summary.json` — current package counts and validation boundary.
- `docs/` — schema, methodology, evaluation protocol, source policy, taxonomy, and limitations.
- `scripts/validate_release.py` — structural, privacy, workbook, and checksum validation.

## Quick start

```bash
python scripts/validate_release.py
python examples/explore_dataset.py
python examples/load_questions.py
```

## Intended uses

This package supports **non-commercial** academic research, semiconductor education, model comparison, knowledge-base construction, RAG prototyping and methods development. WP1 may support knowledge augmentation; WP2 is designed for transparent evaluation and research into scoring, but its publicly exposed answers and rubrics must not be misrepresented as an unseen test. Adaptations and redistribution remain subject to the applicable licenses, with separate commercial permissions when required.

## Evaluation boundary

Only `item.question`, `item.input_data`, and `item.assumptions` should be provided to an evaluated model under the documented WP2→WP3 contract. Keep `reference_answer`, `rubric`, `criteria`, source metadata, and other non-model-facing fields out of model prompts and retrieval contexts.

Because this distribution contains full answers and rubrics, it is not an unseen held-out test after publication. Use a separate private test set for blind performance claims.

## Licensing

Original WP1/WP2 data and original authored documentation: **[CC BY-NC 4.0](LICENSE-DATA)**. Original software, scripts, examples and authored CI code: **[PolyForm Noncommercial 1.0.0](LICENSE-SOFTWARE)**. These are **non-commercial source-available licenses, not OSI-approved open-source licenses**. The conditions and exceptions differ by license; consult [LICENSING.md](LICENSING.md) and official terms. Additional commercial permissions may be negotiated with the authorized rights holder(s) through [COMMERCIAL-LICENSING.md](COMMERCIAL-LICENSING.md).

**Release owner and licensing representative:** Kain Lu Low, acting on behalf of the authorized licensors for the covered original material.

Dataset contributors and their supplied GitHub identifiers are listed in [CONTRIBUTORS.md](CONTRIBUTORS.md) and the versioned [CITATION.cff](CITATION.cff).

## Review and release status

The 225 WP1 records and 769 WP2 items are human-approved; the public files contain a collection-level `Approved` declaration rather than individual reviewer workflow fields. The release validator checks task profiles, scoring totals, WP1 links and targeted alignment cases; it does **not** prove semantic consistency of every prose rubric, criterion, or technical citation. The WP2 collection completed review under Project B V1.3. Public-package validation confirms structure, linkage, scoring totals, targeted privacy checks, workbook alignment and file checksums; it does not replace scientific interpretation or downstream evaluator calibration.

Third-party textbooks and papers are cited but are not bundled or relicensed. The release owner has reported obtaining the required permissions. Source-reference/locator named-work consistency has been checked against the cited editions at item level. Local publication-readiness validation passes; confirm remote GitHub CI after upload.

## Distribution schema policy

This release omits individual contributor IDs, reviewer comments/status, historical generator statuses, internal timestamps, local mirrored-file hashes and duplicate quality-warning fields. It keeps all technical assessment text, numerical scoring rules, source references and WP1-to-WP2 links. Contributor credit is provided centrally in `CONTRIBUTORS.md` and `CITATION.cff`. The public workbook includes a blank external-user response template, not internal results.

The public files are not substitutes for the unchanged private Project B reviewed masters; `scripts/validate_release.py` verifies the derived public schema.
