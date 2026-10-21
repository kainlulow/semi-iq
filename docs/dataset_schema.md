# Public dataset format (V1.0.0)

The public JSON is a *distribution schema*, intentionally distinct from Project B review/master Draft and recommendation formats. The authoritative approved masters and reviewer records are retained privately and unchanged.

## WP1 (`data/v1.0/wp1_knowledge.json`)

`records` contains 225 knowledge records. Each has a stable `record_id`, module and subdomain IDs/names, `knowledge_title`, `knowledge_summary`, `key_concepts`, `knowledge_level`, `keywords`, `prerequisite_knowledge`, `related_topics`, `source_reference` and `source_locator`. The top level includes `schema_version`, `project` and `dataset_release`. Dataset-level approval is recorded once in `dataset_release.approval_status`.

The public file excludes per-record `contributor`, `notes`, `review_status`, `reviewer_comments` and repeated `intended_use`, and excludes private collection review metadata. See `CONTRIBUTORS.md` and the general intended uses in the README.

## WP2 (`data/v1.0/wp2_benchmark.json`)

`items` contains 769 objects with `wp1_link` (stable exact WP1 identity), `item` (technical assessment content) and `criteria` (1,247 scoring rules in total). Every item includes a question, `input_data`, `assumptions`, reference answer, rubric, scoring profile, difficulty, technical-source reference and locator, and stable WP1 linkage. Criterion extensions include conceptual score anchors, grading policy, numeric tolerance and accepted alternatives where provided.

Internal `student_owner`, item-level review statuses/comments, empty dataset warnings, legacy `Draft` generator statuses, timestamps, generator validation and redundant versions/domain are **not published**. `wp1_link.review_status` is also not published; the linked identity remains exact.

The public dataset is **not** an input to the unchanged internal `validate_project_b.js` master contract. Use `scripts/validate_release.py` for this public projection. A private master-to-public transformation audit records the permitted differences and protects technical content.

## Excel convenience projection

`wp2_benchmark.xlsx` contains `Instructions`, `Items`, `Criteria`, and the **empty optional response-entry template** `Responses`. It exposes selected fields rather than the complete nested scoring policy. Public JSON is authoritative.
