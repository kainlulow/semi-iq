# Evaluation protocol and protected fields

1. Load WP2 entries and select a documented evaluation subset/version.
2. Build the evaluated-model request **only** from `item.question`, `item.input_data`, and `item.assumptions`, retaining legitimate task givens but no hidden provenance.
3. Keep `reference_answer`, `rubric`, `criteria`, `source_reference`, `source_locator`, and all other non-model-facing metadata isolated from the model and any retrieval context.
4. Record the model identifier/configuration, prompt template, decoding settings, retrieval setup, repetition count, run IDs and response statuses.
5. Score using a separate evaluator with profile-appropriate logic and expert adjudication where needed; score semantic conceptual equivalence fairly.
6. Report denominators, incomplete/error runs, uncertainty and any potential data contamination.

**Important:** This distribution provides input-field guidance, *not* a verified WP3 runtime, RAG isolation test, scorer calibration or run-completeness audit. Because the answers and criteria are public if the full dataset is published, this collection cannot credibly serve as an unseen held-out test. Maintain distinct nonpublic evaluation items if blind comparison is required.
