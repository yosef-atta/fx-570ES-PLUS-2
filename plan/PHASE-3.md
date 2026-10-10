# PHASE-3.md — Advanced Calculator Modes

**Project:** Scientific Calculator — fx-570ES PLUS-2 Inspired  
**Phase:** 3 — Advanced Calculator Modes  
**Status:** Completed  
**Target:** Windows 10/11  
**Python:** 3.10.11  
**Dependencies:** PySide6, SymPy, pytest, uv  

---

## 1. Objective

Implement all remaining documented calculator modes and advanced capabilities of the Casio fx-570ES PLUS-2 (2nd Edition), expanding beyond COMP mode to achieve full multi-mode calculator parity.

Phase 3 implements all 7 additional calculation modes:
1. **CMPLX (Mode 2):** Complex number arithmetic, polar/rectangular forms ($a+bi \leftrightarrow r\angle\theta$), modulus ($\text{Abs}$), argument ($\text{arg}$), and conjugate ($\text{Conjg}$).
2. **STAT (Mode 3):** Statistical data editor, single-variable statistics ($1\text{-VAR}$), 7 regression models ($A+BX, _+CX^2, \ln X, e^X, A\cdot B^X, A\cdot X^B, 1/X$), summation metrics, and normal distributions ($P, Q, R, \blacktriangleright t$).
3. **BASE-N (Mode 4):** Binary, octal, decimal, hexadecimal integer arithmetic, twos-complement negative numbers, logical operations ($\text{and}, \text{or}, \text{xor}, \text{xnor}, \text{Not}, \text{Neg}$), and base overrides.
4. **EQN (Mode 5):** Simultaneous linear equation systems (2 and 3 unknowns) and polynomial root solving (quadratic $aX^2+bX+c=0$ and cubic $aX^3+bX^2+cX+d=0$) with real and complex roots and parabola vertex coordinates.
5. **MATRIX (Mode 6):** Matrix editing for memories $\text{MatA}, \text{MatB}, \text{MatC}$ (dimensions $1\times 1$ to $3\times 3$), arithmetic, determinant ($\text{det}$), transpose ($\text{Trn}$), inversion ($\text{Mat}^{-1}$), powers ($\text{Mat}^2, \text{Mat}^3$), and $\text{MatAns}$.
6. **TABLE (Mode 7):** Table generator for functions $f(X)$ and $g(X)$ over configurable range ($\text{Start}, \text{End}, \text{Step}$) with scrollable tabular display.
7. **VECTOR (Mode 8):** Vector editing for $\text{VctA}, \text{VctB}, \text{VctC}$ (2D and 3D), vector arithmetic, dot product ($\text{Dot}$), cross product ($\times$), magnitude ($\text{Abs}$), and $\text{VctAns}$.
8. **Scientific Constants & Metric Conversions:**
   - 40 built-in scientific constants (via SHIFT + 7 `CONST`).
   - 40 built-in metric conversion pairs (via SHIFT + 8 `CONV`).

---

## 2. Architecture & Subsystem Layout

Phase 3 builds on the extensible `src/core/` and `src/core/math/` architecture established in Phases 1 and 2, adding dedicated mode engines and specialized editor UI panels.

```text
fx-570ES-PLUS-2/
│
├── src/
│   ├── app.py
│   │
│   ├── core/
│   │   ├── action.py
│   │   ├── state.py                # Enhanced with mode-specific state & sub-editors
│   │   ├── controller.py           # Multi-mode lifecycle and menu dispatch
│   │   ├── key_registry.py         # Full 8-mode key resolvers
│   │   │
│   │   └── modes/                  # NEW: Advanced Mode Engines
│   │       ├── __init__.py
│   │       ├── complex_engine.py   # CMPLX calculations and polar/rectangular conversion
│   │       ├── stat_engine.py      # STAT calculations, data tables, regressions, normal dist
│   │       ├── basen_engine.py     # BASE-N integer arithmetic, bitwise logic, conversions
│   │       ├── eqn_engine.py       # EQN simultaneous linear and polynomial solvers
│   │       ├── matrix_engine.py    # MATRIX dimensions, operations, det, Trn, inverse
│   │       ├── table_engine.py     # TABLE function generator f(x), g(x)
│   │       ├── vector_engine.py    # VECTOR 2D/3D operations, dot/cross products
│   │       └── constants_conv.py   # 40 Scientific Constants & 40 Metric Conversions
│   │
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── calculator_display.py   # Multi-mode indicators and table/matrix view switching
│   │   ├── table_view.py           # NEW: Grid editor for STAT, MATRIX, VECTOR, TABLE
│   │   ├── natural_canvas.py
│   │   └── keypad.py
│   │
│   └── input/
│       └── keyboard.py
│
├── test/
│   ├── conftest.py
│   ├── test_cmplx.py               # CMPLX mode tests
│   ├── test_stat.py                # STAT mode and regression tests
│   ├── test_basen.py               # BASE-N calculations and bitwise tests
│   ├── test_eqn.py                 # EQN linear systems and polynomial tests
│   ├── test_matrix.py              # MATRIX operations and properties tests
│   ├── test_table.py               # TABLE generation tests
│   ├── test_vector.py              # VECTOR dot/cross product tests
│   ├── test_constants_conv.py      # Scientific constants and metric conversions
│   └── test_mode_transitions.py    # Multi-mode switching and state isolation tests
│
└── plan/
    ├── PHASE-1.md
    ├── PHASE-2.md
    └── PHASE-3.md
```

### Dependency Flow in Multi-Mode Operation

```text
Keypad / Keyboard Action
           │
           ▼
    Controller Dispatch
           │
  ┌────────┼────────────────────────────────────────┐
  ▼        ▼                                        ▼
COMP     CMPLX / BASE-N / STAT                 MATRIX / EQN / TABLE / VECTOR
Engine   Direct Mode Engines                   Table / Grid Sub-Editor
  │        │                                        │
  └────────┴───────────────────┬────────────────────┘
                               ▼
                    Mode Execution Result
                               ▼
                    Calculator State Refresh
                               ▼
               UI Display (LCD / Grid / Table)
```

---

## 3. Implementation Steps

### Step 1 — Mode Architecture & State Expansion

**Target Files:**
- `src/core/state.py`
- `src/core/modes/__init__.py`
- `test/test_mode_transitions.py`

**Design Specifications:**
1. Expand `CalculatorState` to manage mode-specific active structures:
   - `complex_format: str = "a+bi"` (`"a+bi"` or `"r∠θ"`).
   - `base_n_mode: str = "DEC"` (`"DEC"`, `"HEX"`, `"BIN"`, `"OCT"`).
   - `stat_type: str | None = None` (selected regression model).
   - `stat_frequency_on: bool = False` (configured in SETUP).
   - `table_editor_active: bool = False` (whether display shows standard LCD or table/grid editor).
   - `active_sub_mode: str | None = None` (e.g. EQN type 1-4, STAT 1-8).
2. Mode Transition Isolation:
   - Switching modes via MODE menu clears transient expressions and resets sub-editors.
   - Preserves independent memory and variables where documented.
   - Display indicators automatically show active mode badge (`CMPLX`, `STAT`, `BASE-N`, `MAT`, `VCT`).

**Acceptance Criteria:**
- Calculator switches between all 8 modes seamlessly.
- Each mode maintains isolated operational state.

---

### Step 2 — CMPLX Mode (Complex Number Arithmetic & Polar Form)

**Target Files:**
- `src/core/modes/complex_engine.py`
- `src/core/math/tokens.py`
- `src/core/math/lexer.py`
- `src/core/math/evaluator.py`
- `test/test_cmplx.py`

**Design Specifications:**
1. **Imaginary Unit $i$:**
   - In CMPLX mode, pressing `ENG` inserts imaginary unit `i` (SymPy `sp.I`).
   - Supports arithmetic with complex numbers: $(2 + 3i) + (4 - 5i) = 6 - 2i$, $(1 + i)(1 - i) = 2$.
   - Powers and fractions with $i$: $\frac{1}{i} = -i$, $(1+i)^2 = 2i$.
2. **Polar Representation ($r\angle\theta$):**
   - Angle symbol `∠` (via SHIFT + `(-)` / angle token).
   - Inputting polar coordinates: $2\angle 45^\circ \rightarrow \sqrt{2} + \sqrt{2}i$.
   - Respects active angle unit (`DEG`, `RAD`, `GRA`).
3. **CMPLX Menu (SHIFT + 2 `CMPLX`):**
   - `1: arg` — Argument / phase angle $\theta = \text{atan2}(b, a)$ in current angle unit.
   - `2: Conjg` — Complex conjugate $\overline{a + bi} = a - bi$.
   - `3: ⯈r∠θ` — Formats/converts result to polar notation.
   - `4: ⯈a+bi` — Formats/converts result to rectangular notation.
4. **Modulus / Absolute Value:**
   - $\text{Abs}(a + bi) = \sqrt{a^2 + b^2}$.

**Acceptance Criteria:**
- Accurate complex arithmetic in both rectangular and polar forms.
- Full support for $\text{arg}$, $\text{Conjg}$, $\text{Abs}$, and mode conversions.

---

### Step 3 — STAT Mode (Statistics, Regression Models & Distributions)

**Target Files:**
- `src/core/modes/stat_engine.py`
- `src/ui/table_view.py`
- `test/test_stat.py`

**Design Specifications:**
1. **Model Selection Menu (MODE 3):**
   - `1: 1-VAR` (Single variable)
   - `2: A+BX` (Linear)
   - `3: _+CX²` (Quadratic)
   - `4: ln X` (Logarithmic)
   - `5: e^X` (Exponential)
   - `6: A•B^X` (Power)
   - `7: A•X^B` (Geometric)
   - `8: 1/X` (Inverse)
2. **Data Editor Grid:**
   - Columns: `X` (and `FREQ` if enabled in SETUP), or `X`, `Y` (and `FREQ`).
   - Interactive cell editing with navigation arrows (▲, ▼, ◀, ▶), `DEL` to delete row, number input + `=` to commit cell value.
   - Pressing `AC` exits editor to STAT calculation screen without losing entered data.
3. **Statistical Calculations (SHIFT + 1 `STAT` Menu):**
   - `1: Type` — Reopen model selection.
   - `2: Data` — Return to data table editor.
   - `3: Sum` — $\sum x^2, \sum x, n$ (and $\sum y^2, \sum y, \sum xy, \sum x^3, \sum x^4, \sum x^2 y$ for 2-variable).
   - `4: Var` — Sample mean $\bar{x}, \bar{y}$, population std dev $\sigma_x, \sigma_y$, sample std dev $s_x, s_y$.
   - `5: Reg` — Regression coefficients $A, B, C$, correlation coefficient $r$, estimate functions $\hat{x}, \hat{y}$.
   - `6: MinMax` — $\min X, \max X, \min Y, \max Y$.
4. **Normal Probability Distributions:**
   - $P(t) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{t} e^{-u^2/2} du$
   - $Q(t) = \frac{1}{\sqrt{2\pi}} \int_{0}^{t} e^{-u^2/2} du$
   - $R(t) = \frac{1}{\sqrt{2\pi}} \int_{t}^{\infty} e^{-u^2/2} du$
   - Standardized variate: $t = \frac{X - \bar{x}}{\sigma_x}$ (via $\blacktriangleright t$).

**Acceptance Criteria:**
- Accurate regression parameter fitting matching Casio standard test datasets.
- Clean data entry table and seamless transition between editor and calculation screen.

---

### Step 4 — BASE-N Mode (Binary, Octal, Decimal, Hexadecimal & Logic)

**Target Files:**
- `src/core/modes/basen_engine.py`
- `test/test_basen.py`

**Design Specifications:**
1. **Bases & Limits:**
   - `DEC`: Decimal (signed 32-bit: $-2,147,483,648$ to $2,147,483,647$).
   - `HEX`: Hexadecimal (digits `0–9`, `A–F`, 8 hex digits, twos-complement).
   - `BIN`: Binary (up to 16/32 bits, twos-complement).
   - `OCT`: Octal (up to 11 digits).
2. **Direct Base Switching Keys:**
   - `x²` $\rightarrow$ `DEC`
   - `x^` $\rightarrow$ `HEX`
   - `log` $\rightarrow$ `BIN`
   - `ln` $\rightarrow$ `OCT`
3. **Hexadecimal Digit Input:**
   - Dedicated key inputs for digits `A, B, C, D, E, F` via keys `(-)`, `°'`, `hyp`, `sin`, `cos`, `tan` without needing ALPHA.
4. **Bitwise Logic Operations (SHIFT + 3 `BASE` Menu):**
   - `and`, `or`, `xor`, `xnor`, `Not`, `Neg`.
5. **Prefix Base Overrides:**
   - `d` (decimal), `h` (hex), `b` (binary), `o` (octal) allow mixing bases in one calculation: e.g. `d10 + b1010` in HEX displays `14`.

**Acceptance Criteria:**
- Precise twos-complement arithmetic across all 4 bases.
- Bitwise logical operations strictly adhere to 32-bit binary specifications.

---

### Step 5 — EQN Mode (Equation Systems & Polynomial Solvers)

**Target Files:**
- `src/core/modes/eqn_engine.py`
- `test/test_eqn.py`

**Design Specifications:**
1. **Equation Types (MODE 5):**
   - `1: anX + bnY = cn` — $2 \times 2$ simultaneous linear equations.
   - `2: anX + bnY + cnZ = dn` — $3 \times 3$ simultaneous linear equations.
   - `3: aX² + bX + c = 0` — Quadratic polynomial.
   - `4: aX³ + bX² + cX + d = 0` — Cubic polynomial.
2. **Coefficient Grid Input:**
   - Interactive coefficient matrix view. Pressing number + `=` enters each coefficient.
3. **Solution Display & Navigation:**
   - Linear systems: displays $X=$, $Y=$ (and $Z=$).
     - Detects `Infinite Sol` (infinite solutions) and `No Solution`.
   - Polynomials:
     - Real and complex roots ($X_1, X_2$, and $X_3$).
     - Quadratic equations: displays vertex coordinates:
       $X\text{-value of Minimum/Maximum} = -\frac{b}{2a}$,
       $Y\text{-value of Minimum/Maximum} = c - \frac{b^2}{4a}$.

**Acceptance Criteria:**
- Accurate root extraction for real and complex roots.
- Proper singularity detection (`No Solution`, `Infinite Sol`).

---

### Step 6 — MATRIX Mode (Matrix Operations & Algebra)

**Target Files:**
- `src/core/modes/matrix_engine.py`
- `test/test_matrix.py`

**Design Specifications:**
1. **Matrix Storage & Dimensions:**
   - 3 matrix registers: $\text{MatA}, \text{MatB}, \text{MatC}$.
   - Supported dimensions: $m \times n$ where $1 \le m, n \le 3$ ($3\times 3, 3\times 2, 3\times 1, 2\times 3, 2\times 2, 2\times 1, 1\times 3, 1\times 2, 1\times 1$).
2. **Matrix Editor:**
   - Dimensional selection menu followed by grid cell editing.
3. **Matrix Operations (SHIFT + 4 `MATRIX` Menu):**
   - Matrix arithmetic: $\text{MatA} + \text{MatB}, \text{MatA} - \text{MatB}, \text{MatA} \times \text{MatB}$, scalar multiplication $2 \times \text{MatA}$.
   - Determinant: $\text{det}(\text{MatA})$.
   - Transpose: $\text{Trn}(\text{MatA})$.
   - Inversion: $\text{MatA}^{-1}$ (via `x⁻¹` key).
   - Matrix Powers: $\text{MatA}^2, \text{MatA}^3$.
   - Matrix Answer: $\text{MatAns}$ automatically updated after calculation.
   - Dimension mismatch raises `Dim ERROR`. Singular matrix inversion raises `Math ERROR`.

**Acceptance Criteria:**
- Accurate matrix multiplications, determinants, and matrix inverses.
- Exact dimension validation and error reporting.

---

### Step 7 — TABLE Mode (Function Table Generation)

**Target Files:**
- `src/core/modes/table_engine.py`
- `test/test_table.py`

**Design Specifications:**
1. **Function Definition:**
   - Prompts for $f(X)$ using variable $X$.
   - If enabled in SETUP (`TABLE: f(x), g(x)`), prompts for second function $g(X)$.
2. **Range Prompts:**
   - `Start?` — initial value of $X$ (default 1).
   - `End?` — final value of $X$ (default 5).
   - `Step?` — step interval $\Delta X$ (default 1).
   - Total generated rows limit: 30 rows max (exceeding raises `Insufficient MEM`).
3. **Tabular Results Display:**
   - Scrollable table displaying columns `Row`, `X`, `F(X)` (and `G(X)`).
   - Displays exact and decimal values with cursor selection.

**Acceptance Criteria:**
- Table generation matches official step calculation and limits.
- Supports both single function and dual function setups.

---

### Step 8 — VECTOR Mode (Vector Operations & Geometry)

**Target Files:**
- `src/core/modes/vector_engine.py`
- `test/test_vector.py`

**Design Specifications:**
1. **Vector Storage & Dimensions:**
   - 3 vector registers: $\text{VctA}, \text{VctB}, \text{VctC}$.
   - Dimensions: 2D ($1\times 2$) or 3D ($1\times 3$).
2. **Vector Operations (SHIFT + 5 `VECTOR` Menu):**
   - Vector addition and subtraction: $\text{VctA} + \text{VctB}, \text{VctA} - \text{VctB}$.
   - Scalar multiplication: $3 \times \text{VctA}$.
   - Dot Product: $\text{VctA} \cdot \text{VctB}$ (via `Dot` token).
   - Cross Product: $\text{VctA} \times \text{VctB}$ (using $\times$ operator).
   - Magnitude / Absolute value: $\text{Abs}(\text{VctA}) = \sqrt{x^2 + y^2 + z^2}$.
   - Vector Answer: $\text{VctAns}$ updated after each vector calculation.

**Acceptance Criteria:**
- Accurate 2D and 3D dot and cross products.
- Error checking on dimension mismatches (`Dim ERROR`).

---

### Step 9 — Scientific Constants & Metric Conversions

**Target Files:**
- `src/core/modes/constants_conv.py`
- `test/test_constants_conv.py`

**Design Specifications:**
1. **40 Scientific Constants (SHIFT + 7 `CONST`):**
   - Full precision CODATA constants matching Casio reference manual:
     - `01`: $mp$ (proton mass, $1.672621637 \times 10^{-27}\text{ kg}$)
     - `02`: $mn$ (neutron mass, $1.674927211 \times 10^{-27}\text{ kg}$)
     - `03`: $me$ (electron mass, $9.10938215 \times 10^{-31}\text{ kg}$)
     - `04`: $m\mu$ (muon mass, $1.88353130 \times 10^{-28}\text{ kg}$)
     - `05`: $a_0$ (Bohr radius, $5.2917720859 \times 10^{-11}\text{ m}$)
     - `06`: $h$ (Planck constant, $6.62606896 \times 10^{-34}\text{ J}\cdot\text{s}$)
     - `07`: $\mu_N$ (Nuclear magneton, $5.05078324 \times 10^{-27}\text{ J/T}$)
     - `08`: $\mu_B$ (Bohr magneton, $9.27400915 \times 10^{-24}\text{ J/T}$)
     - ... up to `40`: $\lambda_c$ (neutron Compton wavelength).
   - Two-digit number input prompt (`01` to `40`) inserts the constant symbol and value.
2. **40 Metric Conversions (SHIFT + 8 `CONV`):**
   - 20 reciprocal conversion pairs matching official manual:
     - `01/02`: $\text{in} \rightarrow \text{cm}$ / $\text{cm} \rightarrow \text{in}$
     - `03/04`: $\text{ft} \rightarrow \text{m}$ / $\text{m} \rightarrow \text{ft}$
     - `05/06`: $\text{yd} \rightarrow \text{m}$ / $\text{m} \rightarrow \text{yd}$
     - `07/08`: $\text{mile} \rightarrow \text{km}$ / $\text{km} \rightarrow \text{mile}$
     - `09/10`: $\text{n mile} \rightarrow \text{m}$ / $\text{m} \rightarrow \text{n mile}$
     - `11/12`: $\text{acre} \rightarrow \text{m}^2$ / $\text{m}^2 \rightarrow \text{acre}$
     - `13/14`: $\text{gal (US)} \rightarrow \text{L}$ / $\text{L} \rightarrow \text{gal (US)}$
     - `15/16`: $\text{gal (UK)} \rightarrow \text{L}$ / $\text{L} \rightarrow \text{gal (UK)}$
     - `17/18`: $\text{pc} \rightarrow \text{km}$ / $\text{km} \rightarrow \text{pc}$
     - `19/20`: $\text{km/h} \rightarrow \text{m/s}$ / $\text{m/s} \rightarrow \text{km/h}$
     - `21/22`: $\text{oz} \rightarrow \text{g}$ / $\text{g} \rightarrow \text{oz}$
     - `23/24`: $\text{lb} \rightarrow \text{kg}$ / $\text{kg} \rightarrow \text{lb}$
     - `25/26`: $\text{atm} \rightarrow \text{Pa}$ / $\text{Pa} \rightarrow \text{atm}$
     - `27/28`: $\text{mmHg} \rightarrow \text{Pa}$ / $\text{Pa} \rightarrow \text{mmHg}$
     - `29/30`: $\text{hp} \rightarrow \text{kW}$ / $\text{kW} \rightarrow \text{hp}$
     - `31/32`: $\text{kgf/cm}^2 \rightarrow \text{Pa}$ / $\text{Pa} \rightarrow \text{kgf/cm}^2$
     - `33/34`: $\text{kgf}\cdot\text{m} \rightarrow \text{J}$ / $\text{J} \rightarrow \text{kgf}\cdot\text{m}$
     - `35/36`: $\text{lbf/in}^2 \rightarrow \text{kPa}$ / $\text{kPa} \rightarrow \text{lbf/in}^2$
     - `37/38`: $^\circ\text{F} \rightarrow ^\circ\text{C}$ / $^\circ\text{C} \rightarrow ^\circ\text{F}$
     - `39/40`: $\text{J} \rightarrow \text{cal}$ / $\text{cal} \rightarrow \text{J}$

**Acceptance Criteria:**
- Exact numerical accuracy matching Casio official conversion factor table.
- Smooth modal prompt workflow (`CONST 01-40`, `CONV 01-40`).

---

### Step 10 — UI Sub-Editors & Multi-Mode Integration

**Target Files:**
- `src/ui/table_view.py`
- `src/ui/calculator_display.py`
- `src/core/controller.py`
- `test/test_integration.py`

**Design Specifications:**
1. Reusable table/matrix grid view widget (`TableView`) embedded into display frame when table/matrix modes are active.
2. Full keyboard and mouse grid navigation:
   - Tab / Enter / Arrow keys to traverse cells.
   - Live cell edit box with instant update.
3. Controller seamlessly handles:
   - Dynamic mode-specific key menus: SHIFT+1 (STAT), SHIFT+2 (CMPLX), SHIFT+3 (BASE), SHIFT+4 (MATRIX), SHIFT+5 (VECTOR), SHIFT+7 (CONST), SHIFT+8 (CONV).
   - Full regression test execution across all 8 modes.

**Acceptance Criteria:**
- Zero unimplemented keys remain across any mode.
- Complete visual and functional fidelity across all 8 modes.

---

## 4. Verification & Testing Matrix

| Mode | Test Operation | Expected Result |
|---|---|---|
| **CMPLX** | `(2 + 3i) × (4 + 5i) =` | `-7 + 22i` |
| **CMPLX** | `Abs(3 + 4i) =` | `5` |
| **CMPLX** | `arg(1 + i) =` (DEG) | `45` |
| **CMPLX** | `Conjg(2 + 3i) =` | `2 - 3i` |
| **STAT** | 1-VAR: Data `{2, 4, 6, 8}` | $\bar{x} = 5, \sigma_x = 2.236067977, n = 4$ |
| **STAT** | A+BX: Data `(1, 2), (2, 4), (3, 6)` | $A = 0, B = 2, r = 1$ |
| **BASE-N** | HEX: `A + F =` | `19` |
| **BASE-N** | BIN: `1010 and 1100 =` | `1000` |
| **EQN** | $2X + 3Y = 8$, $X - Y = -1$ | $X = 1, Y = 2$ |
| **EQN** | $X^2 - 5X + 6 = 0$ | $X_1 = 3, X_2 = 2$ |
| **MATRIX** | $\text{MatA} = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$, $\text{det}(\text{MatA})$ | `-2` |
| **MATRIX** | $\text{MatA}^{-1}$ | $\begin{pmatrix} -2 & 1 \\ 1.5 & -0.5 \end{pmatrix}$ |
| **TABLE** | $f(X) = X^2 + 1$, Start 1, End 3, Step 1 | $X=\{1, 2, 3\}, f(X)=\{2, 5, 10\}$ |
| **VECTOR** | $\text{VctA}=(1, 2, 3), \text{VctB}=(4, 5, 6), \text{VctA} \cdot \text{VctB}$ | `32` |
| **VECTOR** | $\text{VctA} \times \text{VctB}$ | $(-3, 6, -3)$ |
| **CONST** | `CONST 01` (proton mass) | $1.672621637 \times 10^{-27}$ |
| **CONV** | `10 CONV 01` ($10\text{ in} \rightarrow \text{cm}$) | $25.4$ |

---

## 5. Definition of Done for Phase 3

Phase 3 is complete only when:

1. **All 8 Modes Operational:** COMP, CMPLX, STAT, BASE-N, EQN, MATRIX, TABLE, and VECTOR function strictly according to Casio fx-570ES PLUS-2 specifications.
2. **Sub-Editors Complete:** Data entry tables and matrix/equation coefficient editors operate with full mouse and keyboard interaction.
3. **Constants & Conversions Active:** All 40 scientific constants and 40 metric conversions compute accurately.
4. **No Deferred Keys Remain:** Every physical key and alternate function (SHIFT/ALPHA) is fully wired and functional.
5. **Automated Test Coverage:**
   - 100% pass rate across the entire test suite (all previous tests + all new mode tests).
   - Zero test regressions.
6. **Task Tracking:** `TASKS.md` Phase 3 items are updated only after full verification.
