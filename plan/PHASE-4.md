# PHASE-4.md — Compatibility & Quality Assurance

**Project:** Scientific Calculator — fx-570ES PLUS-2 Inspired  
**Phase:** 4 — Compatibility & Quality Assurance  
**Status:** Completed  
**Target:** Windows 10/11  
**Python:** 3.10.11  
**Dependencies:** PySide6, SymPy, pytest, uv  

---

## 1. Objective

Validate and certify calculator behavior, stability, precision, and usability against the official Casio fx-570ES PLUS-2 (2nd Edition) user's guide across all 8 operating modes.

### Key Quality Assurance Criteria:
1. **Full Functional & Key Audit:**
   - Audit every physical key across primary, SHIFT, and ALPHA bindings.
   - Audit all 8 operating modes: `COMP`, `CMPLX`, `STAT`, `BASE-N`, `EQN`, `MATRIX`, `TABLE`, `VECTOR`.
   - Audit all menus (`MODE`, `SETUP`, `CLR`, `CMPLX`, `STAT`, `BASE`, `EQN`, `MATRIX`, `VECTOR`).
   - Audit `SETUP` configurations: `MthIO`/`LineIO`, angle units (`DEG`/`RAD`/`GRA`), number formats (`Norm 1/2`, `Fix 0~9`, `Sci 0~9`), fraction styles (`ab/c` vs `d/c`), STAT frequency (`ON`/`OFF`), CMPLX format (`a+bi` vs `r∠θ`).
2. **Mathematical Accuracy & Precision:**
   - Verify 10-digit standard display and 15-digit internal precision.
   - Verify exact symbolic calculations (fractions, $\pi$, $e$, $\sqrt{n}$, mixed fractions).
   - Verify rounding rules for Fix, Sci, Norm 1, Norm 2, and engineering notation.
   - Verify trigonometric, hyperbolic, exponential, logarithmic, and combinatoric identities.
3. **Error Boundaries & Recovery:**
   - Verify all documented error types: `Math ERROR`, `Syntax ERROR`, `Dim ERROR`, `Argument ERROR`, `Can't Solve`, `Insufficient MEM`.
   - Verify error locus navigation: `◀` and `▶` restore cursor position to the exact error location.
   - Verify that `AC` clears error state and restores the expression and workspace.
4. **Desktop UI, Keyboard & Mouse Interaction:**
   - Verify mouse clicks for every button on keypad.
   - Verify full physical keyboard integration including numpad, function keys, and quick shortcuts (`s` for sin, `c` for cos, `t` for tan, `l` for ln, `r` for sqrt, `!` for factorial, `i` for imag).
   - Verify window resizing and dynamic layout scaling without clipping.
5. **Stress Testing & Stability:**
   - Rapid sequential input stress testing (high keystroke frequency without race conditions).
   - Deep nested parentheses and multi-statement expressions (`:` separator).
   - Zero memory leaks, clean teardown, and 100% test pass rate across the full regression suite.

---

## 2. Validation Architecture

```text
fx-570ES-PLUS-2/
│
├── src/
│   ├── core/
│   │   ├── controller.py         # Audited for setup prompts, error recovery, multi-statement
│   │   ├── state.py              # Audited for all mode/setup state properties
│   │   ├── key_registry.py       # Audited for 100% active physical keys
│   │   └── math/                 # Precision, rounding, and error reporting
│   ├── ui/
│   │   ├── main_window.py        # Audited for layout scaling and table/display switching
│   │   └── keypad.py             # Audited for all button click handlers
│   └── input/
│       └── keyboard.py           # Enhanced with quick scientific shortcuts
│
└── test/
    ├── test_qa_audit.py          # Functional audit covering all modes, menus, and setups
    ├── test_accuracy_precision.py# Mathematical precision, exact forms, rounding
    ├── test_boundary_errors.py   # Boundary conditions, division by zero, error locus
    ├── test_ui_stress.py         # Window resize scaling, rapid input, multi-statements
    └── ...                       # All existing test suites (182 tests)
```

---

## 3. Step-by-Step Execution Plan

- [x] **Step 1:** Establish dedicated feature branch `feature/phase-4-compatibility-and-qa`.
- [x] **Step 2:** Audit and enhance `SETUP` menu options in `src/core/controller.py` (prompts for `Fix 0~9`, `Sci 0~9`, `Norm 1~2`, `ab/c` vs `d/c`, `STAT Frequency On/Off`).
- [x] **Step 3:** Expand physical keyboard shortcuts in `src/input/keyboard.py` (`!`, `s`, `c`, `t`, `l`, `r`, `i`).
- [x] **Step 4:** Implement `test/test_qa_audit.py` to test all menus, modes, setup options, and key combinations.
- [x] **Step 5:** Implement `test/test_accuracy_precision.py` to test precision, exact arithmetic, rounding, and identities.
- [x] **Step 6:** Implement `test/test_boundary_errors.py` to test all error classes, overflow/underflow, and goto error locus.
- [x] **Step 7:** Implement `test/test_ui_stress.py` to test window scaling, rapid keystrokes, and multi-statement chains.
- [x] **Step 8:** Run the complete test suite ensuring 100% pass rate (182/182 passing).
- [x] **Step 9:** Update `TASKS.md` and mark Phase 4 completed.
- [x] **Step 10:** Git Commit, Push, Open PR with `gh`, Merge, and Report.
