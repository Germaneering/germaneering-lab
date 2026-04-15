# Tasks: Sea Route Service Tester CLI

**Input**: Design documents from `/specs/002-geosearoute-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are required for this feature because the plan and constitution call for test-first development with `unittest` and mocked HTTP behavior.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare packaging, source layout, and test layout for the new dedicated CLI package.

- [ ] T001 Update packaging and `uv` metadata for `geosearoute-cli` in pyproject.toml
- [ ] T002 Create package skeleton files in geosearoute_cli/__init__.py, geosearoute_cli/__main__.py, geosearoute_cli/cli.py, geosearoute_cli/client.py, geosearoute_cli/models.py, and geosearoute_cli/validator.py
- [ ] T003 [P] Create test module skeletons in tests/test_cli.py, tests/test_client.py, tests/test_models.py, and tests/test_validator.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement shared configuration, request/response abstractions, and client infrastructure that all user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T004 [P] Add failing model tests for shared service entities in tests/test_models.py
- [ ] T005 [P] Add failing validation tests for RapidAPI environment handling and numeric guards in tests/test_validator.py
- [ ] T006 Implement shared service entities in geosearoute_cli/models.py
- [ ] T007 Implement shared configuration and numeric validation helpers in geosearoute_cli/validator.py
- [ ] T008 [P] Add failing client tests for fixed RapidAPI endpoint, common headers, and response normalization in tests/test_client.py
- [ ] T009 Implement fixed-endpoint RapidAPI client behavior in geosearoute_cli/client.py

**Checkpoint**: Foundation ready; nearest and solve command work can now proceed.

---

## Phase 3: User Story 1 - Find Nearby Sea Route Access (Priority: P1) 🎯 MVP

**Goal**: Let an operator call `nearest` with latitude, longitude, and optional distance and receive formatted JSON from the service.

**Independent Test**: Run `uv run geosearoute-cli nearest 57.7089 11.9746` with `x_rapidapi_host` and `x_rapidapi_key` set and verify that the command uses the default `distance=500`, sends the RapidAPI headers, and prints pretty JSON on stdout.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Add failing nearest command parser and exit-behavior tests in tests/test_cli.py
- [ ] T011 [P] [US1] Add failing nearest request/response tests in tests/test_client.py

### Implementation for User Story 1

- [ ] T012 [US1] Implement the `NearestQuery` model and defaults in geosearoute_cli/models.py
- [ ] T013 [US1] Implement nearest argument parsing and coordinate validation in geosearoute_cli/cli.py and geosearoute_cli/validator.py
- [ ] T014 [US1] Implement nearest request building and execution in geosearoute_cli/client.py
- [ ] T015 [US1] Wire nearest command dispatch, pretty JSON output, and exit codes in geosearoute_cli/cli.py and geosearoute_cli/__main__.py

**Checkpoint**: User Story 1 should be fully functional and independently testable.

---

## Phase 4: User Story 2 - Solve a Multi-Stop Route (Priority: P2)

**Goal**: Let an operator submit ordered route stops with an optional speed and receive a formatted solved route response.

**Independent Test**: Run `uv run geosearoute-cli solve --stop 11.9746 57.7089 --stop 4.47917 51.9225` with RapidAPI environment variables set and verify that the command sends `speed=24`, preserves stop order as `[[lon, lat], ...]`, and prints pretty JSON on stdout.

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T016 [P] [US2] Add failing solve command parser and ordered-stop tests in tests/test_cli.py
- [ ] T017 [P] [US2] Add failing solve request serialization tests in tests/test_client.py

### Implementation for User Story 2

- [ ] T018 [P] [US2] Implement `StopCoordinate` and `SolveQuery` models in geosearoute_cli/models.py
- [ ] T019 [US2] Implement solve stop parsing, minimum-stop checks, and speed validation in geosearoute_cli/cli.py and geosearoute_cli/validator.py
- [ ] T020 [US2] Implement solve request serialization and execution in geosearoute_cli/client.py
- [ ] T021 [US2] Wire solve command dispatch, formatted output, and exit handling in geosearoute_cli/cli.py and geosearoute_cli/__main__.py

**Checkpoint**: User Stories 1 and 2 should both work independently.

---

## Phase 5: User Story 3 - Recover From Configuration and Input Failures (Priority: P3)

**Goal**: Provide early, actionable feedback for missing RapidAPI variables, malformed inputs, help usage, transport failures, and remote error responses.

**Independent Test**: Run commands with missing `x_rapidapi_host` and `x_rapidapi_key`, malformed coordinates or stops, and mocked non-JSON or non-2xx service responses and verify that stderr messages are actionable and the process exits non-zero.

### Tests for User Story 3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T022 [P] [US3] Add failing configuration and help-output tests in tests/test_cli.py
- [ ] T023 [P] [US3] Add failing transport, non-JSON error, and remote failure tests in tests/test_client.py

### Implementation for User Story 3

- [ ] T024 [US3] Implement early missing-environment and malformed-input failure messaging in geosearoute_cli/cli.py and geosearoute_cli/validator.py
- [ ] T025 [US3] Implement transport and remote error classification plus stderr rendering in geosearoute_cli/client.py and geosearoute_cli/cli.py
- [ ] T026 [US3] Finalize top-level help and command-specific help text in geosearoute_cli/cli.py

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Finish packaging, documentation, and end-to-end validation across all stories.

- [ ] T027 [P] Update exploration documentation and usage examples in README.md
- [ ] T028 [P] Align package metadata, runtime dependency declaration, and console script details in pyproject.toml and geosearoute_cli/__init__.py
- [ ] T029 Validate quickstart and packaging workflow in specs/002-geosearoute-cli/quickstart.md and pyproject.toml

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; starts immediately.
- **Foundational (Phase 2)**: Depends on Setup; blocks all user story work.
- **User Stories (Phases 3-5)**: Depend on Foundational completion.
- **Polish (Phase 6)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational; defines the MVP path.
- **User Story 2 (P2)**: Starts after Foundational; functionally independent of US1 but best implemented after P1 to reduce shared-file churn.
- **User Story 3 (P3)**: Starts after Foundational; can be tested independently but is best sequenced after US1 and US2 because it finalizes shared error behavior in the same files.

### Within Each User Story

- Tests MUST be written and fail before implementation.
- Models before command wiring.
- Validation before request execution.
- Request execution before final CLI dispatch and output wiring.

### Parallel Opportunities

- T003 can run in parallel with T002 once T001 is complete.
- T004 and T005 can run in parallel during the Foundational phase.
- T008 can run in parallel with T006 and T007 after the package skeleton exists.
- T010 and T011 can run in parallel for US1.
- T016 and T017 can run in parallel for US2.
- T018 can run in parallel with T016 and T017 for US2.
- T022 and T023 can run in parallel for US3.
- T027 and T028 can run in parallel during Polish.

---

## Parallel Example: User Story 1

```bash
# Launch nearest-story tests together:
Task: "Add failing nearest command parser and exit-behavior tests in tests/test_cli.py"
Task: "Add failing nearest request/response tests in tests/test_client.py"
```

## Parallel Example: User Story 2

```bash
# Launch solve-story tests and model work together:
Task: "Add failing solve command parser and ordered-stop tests in tests/test_cli.py"
Task: "Add failing solve request serialization tests in tests/test_client.py"
Task: "Implement StopCoordinate and SolveQuery models in geosearoute_cli/models.py"
```

## Parallel Example: User Story 3

```bash
# Launch failure-path tests together:
Task: "Add failing configuration and help-output tests in tests/test_cli.py"
Task: "Add failing transport, non-JSON error, and remote failure tests in tests/test_client.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational.
3. Complete Phase 3: User Story 1.
4. **STOP and VALIDATE**: Run the nearest command flow independently.

### Incremental Delivery

1. Setup + Foundational establish the shared package, validation, and RapidAPI client.
2. Add User Story 1 and validate `nearest` as the MVP.
3. Add User Story 2 and validate multi-stop `solve` without regressing `nearest`.
4. Add User Story 3 and validate all failure and help paths.
5. Finish with documentation and `uv build` / quickstart validation.

### Suggested Delivery Order

1. T001-T009
2. T010-T015
3. T016-T021
4. T022-T026
5. T027-T029

---

## Notes

- Every task follows the required checklist format with task ID, optional parallel marker, optional story label, and file path.
- Tests are included because the constitution and plan make test-first development mandatory.
- The tasks assume a dedicated `geosearoute_cli/` package at repository root and reuse the existing `tests/` directory.
- `uv run` and `uv build` are treated as the primary execution and packaging workflows throughout implementation.