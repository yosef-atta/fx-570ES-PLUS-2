# Scientific Calculator — TASKS.md

## Goal

Build a free, offline, native Windows scientific calculator inspired by the Casio fx-570ES PLUS-2 (2nd Edition).

The application must support all documented calculator functions, familiar key behavior, natural mathematical display, and full keyboard/mouse interaction.

## Tech Stack

- Python 3.10.11
- PySide6 — Native desktop interface
- SymPy — Mathematical computation support
- pytest — Automated testing
- uv — Dependency and project management
- Windows 10/11 — Target platforms

## Project Rules

1. Build our own application, UI, state management, and calculator logic.
2. Do not reuse Casio firmware, ROMs, or third-party calculator implementations.
3. Use documented dependencies from trusted distribution sources.
4. Use the official Casio manual as the functional reference.
5. Every functional feature must have tests.
6. No placeholder buttons in completed features.
7. Keep modules small and avoid unnecessary abstractions.
8. Complete and validate each phase before moving forward.
9. Do not mark tasks complete without working implementation.
10. Maintain a feature checklist covering all documented operations.

---

## Phase 1 — Application Foundation

**Goal:** A functional Windows application with complete calculator controls.

- [x] Establish clean project structure and application entry point.
- [x] Create the calculator window with original styling and familiar key layout.
- [x] Implement the calculator display, menus, and button components.
- [x] Implement keyboard/numpad/mouse input and arrow navigation.
- [x] Implement SHIFT, ALPHA, DEL, AC, MODE, and SETUP interaction states.
- [x] Add initial UI, input, and application-launch tests.

**Done when:** The application launches, every key dispatches the correct action, navigation works, and foundation tests pass.

## Phase 2 — Core Mathematics & Display

**Goal:** A fully usable scientific calculator in COMP mode.

- [x] Build the expression parser, evaluation engine, and error handling.
- [x] Implement arithmetic, parentheses, precedence, fractions, powers, roots, and factorials.
- [x] Implement trigonometric, inverse, hyperbolic, logarithmic, exponential, and related functions.
- [x] Implement mathematical constants, percentages, permutations, combinations, and random functions.
- [x] Implement Natural Textbook Display, cursor editing, and exact/decimal result switching.
- [x] Implement Ans, variable memory, replay/history, DEG/RAD/GRA, Fix/Sci/Norm, and engineering notation.
- [x] Implement remaining COMP operations, including coordinate conversion, DMS, numerical calculus, summation, CALC, and SOLVE.
- [x] Add automated tests for all completed COMP functions.

**Done when:** All documented COMP operations work and their tests pass.

## Phase 3 — Advanced Calculator Modes

**Goal:** Implement all remaining calculation modes.

- [x] CMPLX — Complex number arithmetic and display.
- [x] STAT — Data entry, statistics, regression, and distributions.
- [x] BASE-N — Binary, octal, decimal, hexadecimal, and logical operations.
- [x] EQN — Equation systems and polynomial solving.
- [x] MATRIX — Matrix editing and operations.
- [x] TABLE — Function tables for f(x) and g(x).
- [x] VECTOR — Vector editing and operations.
- [x] Implement scientific constants, metric conversions, and any remaining documented features.
- [x] Add automated tests for every mode.

**Done when:** Every documented calculator mode and operation is implemented and tested.

## Phase 4 — Compatibility & Quality Assurance

**Goal:** Validate calculator behavior and stability.

- [x] Audit all functions, key combinations, menus, and settings against the official manual.
- [x] Verify mathematical accuracy, precision, rounding, and exact result formatting.
- [x] Verify error conditions, boundary cases, and mode transitions.
- [x] Test complete keyboard and mouse workflows.
- [x] Test layout scaling, input speed, and repeated operations.
- [x] Resolve known defects and run the complete regression suite.

**Done when:** The feature checklist is complete, all tests pass, and no known critical defects remain.

## Phase 5 — Windows Release

**Goal:** Deliver a complete Windows desktop application.

- [x] Add persistent preferences and configurable keyboard shortcuts.
- [x] Add application icon, metadata, and version information.
- [x] Package the application for offline Windows use.
- [x] Verify startup and calculator operation on a clean Windows environment.
- [x] Complete dependency/license checks and final release validation.
- [x] Produce the final Windows executable and installation instructions.

**Done when:** The released application installs, launches, and works offline without a separate Python installation.

---

## Completion Criteria

The project is finished only when:

- [x] All documented fx-570ES PLUS-2 features are covered.
- [x] All eight calculation modes work.
- [x] Natural mathematical input/output works.
- [x] All supported keyboard and mouse interactions work.
- [x] Automated tests pass.
- [x] No known critical bugs remain.
- [x] The application runs offline on Windows 10/11.
- [x] A distributable Windows release is available.

## References

Official calculator:
https://www.casio.com/mea-en/scientific-calculators/product.FX-570ESPLUS-2/

Official user guide:
https://www.casio.com/content/dam/casio/global/support/manuals/calculators/pdf/2022/mutual/fx-570ES_991ES_9910NG_PLUS_EN.pdf

## Current Progress

- [x] Initialize uv project.
- [x] Create Python virtual environment.
- [x] Install PySide6, SymPy, and pytest.
- [x] Phase 1 — Application Foundation.
- [x] Phase 2 — Core Mathematics & Display.
- [x] Phase 3 — Advanced Calculator Modes.
- [x] Phase 4 — Compatibility & Quality Assurance.
- [x] Phase 5 — Windows Release.
