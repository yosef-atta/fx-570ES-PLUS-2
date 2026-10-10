# PHASE-2.md — Core Mathematics & Display

**Project:** Scientific Calculator — fx-570ES PLUS-2 Inspired  
**Phase:** 2 — Core Mathematics & Display  
**Status:** Completed  
**Target:** Windows 10/11  
**Python:** 3.10.11  
**Dependencies:** PySide6, SymPy, pytest, uv  

---

## 1. Objective

Build a fully usable scientific calculator in COMP (Computation) mode, achieving complete parity with the documented operations of the Casio fx-570ES PLUS-2 (2nd Edition).

Phase 2 replaces all deferred placeholder actions for standard scientific calculation with a production-grade mathematical engine, full expression parsing, Natural Textbook Display (2D rendering and navigation), exact/decimal result switching, variable/answer memory, calculation replay, numerical calculus, and Casio-standard error handling.

### Phase 2 completion requirements

1. **Expression Parser & AST:** Complete lexing and parsing of mathematical expressions, including implicit multiplication, operator precedence, nested parentheses, and multi-statement expressions (`:`).
2. **Core Evaluation Engine:** High-precision evaluation using SymPy for exact symbolic and rational calculations, seamlessly supporting floating-point fallbacks.
3. **Full Function Parity in COMP Mode:**
   - Arithmetic, powers ($x^2, x^3, x^y$), roots ($\sqrt{\ }, \sqrt[3]{\ }, \sqrt[x]{\ }$), fractions ($\frac{a}{b}, a\frac{b}{c}$), reciprocal ($x^{-1}$), factorials ($x!$).
   - Trigonometric and inverse trigonometric functions ($\sin, \cos, \tan, \sin^{-1}, \cos^{-1}, \tan^{-1}$) in DEG, RAD, and GRA.
   - Hyperbolic and inverse hyperbolic functions ($\sinh, \cosh, \tanh, \sinh^{-1}, \cosh^{-1}, \tanh^{-1}$).
   - Logarithms ($\log_{10}, \log_a(b), \ln$) and exponentials ($10^x, e^x, e$).
   - Mathematical constants ($\pi, e$), percentages ($\%$), combinatorics ($n\text{P}r, n\text{C}r$), and random generators ($\text{Ran}\#, \text{RanInt}\#$).
   - Coordinate conversions ($\text{Pol}, \text{Rec}$) and sexagesimal DMS ($^\circ\ '\ ''$).
   - Numerical calculus: numerical derivative ($\frac{d}{dx}$), numerical integration ($\int$), and summation ($\sum$).
   - Interactive expressions: `CALC` (evaluate with variable substitution) and `SOLVE` (Newton-Raphson root finding for equations).
4. **Natural Textbook Display (MthIO):** 2D visual rendering of fractions, powers, radicals, and integrals with interactive sub-slot cursor editing, plus LineIO mode support.
5. **Display Formatting & S⇔D:** Exact fraction/radical/$\pi$ representations, decimal approximations, Fix (0–9), Sci (0–9), Norm (1/2), Engineering notation (ENG / $\leftarrow$), and one-touch exact/decimal toggle (`S⇔D` and shift `a b/c ⇔ d/c`).
6. **Memory & History:** `Ans`, `PreAns`, variables $A, B, C, D, E, F, X, Y, M$, independent memory accumulation ($M+, M-$), and calculation replay buffer with arrow navigation.
7. **Error System:** Accurate diagnostic errors (`Math ERROR`, `Syntax ERROR`, `Stack ERROR`, `Argument ERROR`, `Can't Solve`) with Casio-style jump-to-error cursor positioning on ◀ / ▶.
8. **Automated Testing:** Exhaustive automated test suite covering all COMP features, edge cases, Casio user manual examples, and numerical accuracy benchmarks.

---

## 2. Architecture & Module Design

Phase 2 introduces a dedicated mathematical subsystem under `src/core/math/` while preserving the clean separation between UI, controller, and state.

```text
fx-570ES-PLUS-2/
│
├── src/
│   ├── app.py
│   │
│   ├── core/
│   │   ├── action.py               # Action definitions (updated with Math actions)
│   │   ├── state.py                # Enhanced state (memory, history, format, display AST)
│   │   ├── controller.py           # Central dispatch and calculation lifecycle
│   │   ├── key_registry.py         # Full COMP action mapping (no deferred COMP keys)
│   │   │
│   │   └── math/                   # NEW: Dedicated Mathematical Engine
│   │       ├── __init__.py
│   │       ├── tokens.py           # Mathematical tokens and token categories
│   │       ├── lexer.py            # Tokenizer with implicit multiplication detection
│   │       ├── ast_nodes.py        # AST nodes (2D structures, operators, functions)
│   │       ├── parser.py           # Pratt / Recursive-descent parser (Casio precedence)
│   │       ├── evaluator.py        # SymPy-backed exact and numerical evaluator
│   │       ├── formatter.py        # Fix/Sci/Norm, ENG, exact S⇔D formatting
│   │       ├── memory.py           # Variables (A-F, X, Y, M), Ans, PreAns, Replay
│   │       ├── calculus.py         # Numerical derivative, integration, summation
│   │       ├── solver.py           # SOLVE (Newton-Raphson) and CALC engines
│   │       ├── coordinates.py      # Pol, Rec, and DMS conversion logic
│   │       └── errors.py           # MathError, SyntaxError, StackError, etc.
│   │
│   ├── ui/
│   │   ├── main_window.py          # Calculator window wiring
│   │   ├── calculator_display.py   # Enhanced display (Natural 2D + LineIO + Indicators)
│   │   ├── natural_canvas.py       # NEW: 2D Natural Textbook rendering component
│   │   ├── keypad.py
│   │   ├── calculator_key.py
│   │   ├── menu_view.py
│   │   └── style.py
│   │
│   └── input/
│       └── keyboard.py             # Extended shortcuts for scientific functions
│
├── test/
│   ├── conftest.py
│   ├── test_lexer.py               # Tokenization tests
│   ├── test_parser.py              # Parsing & precedence tests
│   ├── test_evaluator.py           # Core evaluation & function tests
│   ├── test_trig_log.py            # Trigonometric, hyperbolic, logarithmic tests
│   ├── test_fractions_powers.py    # Fractions, roots, powers, factorials
│   ├── test_memory.py              # Ans, PreAns, variables, M+, RCL/STO
│   ├── test_replay.py              # Replay buffer and editing tests
│   ├── test_formatting.py          # Fix, Sci, Norm, ENG, S⇔D tests
│   ├── test_calculus.py            # Integration, derivative, summation tests
│   ├── test_solve_calc.py          # SOLVE and CALC workflow tests
│   ├── test_coordinates_dms.py     # Pol, Rec, DMS tests
│   ├── test_errors.py              # Error handling and jump-to-error tests
│   ├── test_display_natural.py     # Natural Textbook Display layout tests
│   └── test_comp_manual.py         # Official Casio manual verification suite
│
└── plan/
    ├── PHASE-1.md
    └── PHASE-2.md
```

### Dependency Flow

```text
User Input (Keypad / Keyboard)
           │
           ▼
    Key Registry / Resolver
           │
           ▼
       Controller
           │
   ┌───────┴──────────────────────────┐
   ▼                                  ▼
Editor / Lexer / Parser        Memory / Replay
   │                                  │
   ▼                                  │
AST Model ────────────────────────────┤
   │                                  │
   ▼                                  │
Evaluator (SymPy + Numerical) ◄───────┘
   │
   ▼
Result & Formatter (Exact / S⇔D / Fix / Sci / Norm / ENG)
   │
   ▼
Calculator State Update
   │
   ▼
UI Refresh (Natural Textbook Canvas / LCD Indicators)
```

---

## 3. Detailed Implementation Steps

### Step 1 — Mathematical Tokens, Lexer, and Syntax Tree

**Target Files:**
- `src/core/math/tokens.py`
- `src/core/math/lexer.py`
- `src/core/math/ast_nodes.py`
- `test/test_lexer.py`

**Design Specifications:**
1. Define strongly-typed tokens representing numbers, identifiers, symbols, operators, parentheses, commas, colons, and structured 2D template markers (`FRACTION_START`, `ROOT_START`, etc.).
2. The lexer must handle:
   - Floating-point and integer literals (`123`, `0.456`, `.5`).
   - Exponential notation via key `×10ˣ` (e.g. `2.5e3` or `2.5×10³`).
   - Multi-character function names (`sin`, `cos`, `tan`, `log`, `ln`, `sinh`, `Pol`, etc.).
   - Distinction between unary negative sign (`(−)` / `−`) and subtraction operator (`-`).
   - Semicolon or colon multi-statement separator (`:`).
3. **Implicit Multiplication Resolution:**
   - Number followed by constant/variable: `2π` $\rightarrow$ `2 * π`, `3X` $\rightarrow$ `3 * X`.
   - Number followed by parenthesis: `2(3+4)` $\rightarrow$ `2 * (3+4)`.
   - Closed parenthesis followed by open parenthesis: `(2)(3)` $\rightarrow$ `(2) * (3)`.
   - Closed parenthesis followed by variable/constant: `(2)A` $\rightarrow$ `(2) * A`.
   - Number followed by prefix function: `2sin(30)` $\rightarrow$ `2 * sin(30)`.
   - *Precedence distinction:* Casio treats implicit multiplication before brackets/symbols with higher priority than explicit multiplication/division in operations like `1 ÷ 2π` $= \frac{1}{2\pi}$.

**Acceptance Criteria:**
- Lexer tokenizes arbitrary scientific expressions without character loss.
- Implicit multiplication inserted correctly according to Casio rules.
- Negative numbers correctly distinguished from subtraction.

---

### Step 2 — Expression Parser with Casio Precedence

**Target Files:**
- `src/core/math/parser.py`
- `src/core/math/errors.py`
- `test/test_parser.py`

**Precedence Hierarchy (Casio fx-570ES PLUS Specification):**
1. Functions with parentheses: `sin(`, `cos(`, `log(`, `Pol(`, `d/dx(`, `∫(`, etc.
2. Functions with prefix values: Coordinate prefix, etc.
3. Postfix operators: Powers ($x^2, x^3, x^y$), roots ($\sqrt{\ }, \sqrt[3]{\ }, \sqrt[x]{\ }$), factorials ($!$), degrees/minutes/seconds ($^\circ\ '\ ''$), percentages ($\%$).
4. Fractions: $\frac{a}{b}$.
5. Prefix symbol: Unary negative sign `(−)`.
6. Statistical estimated values (in STAT mode).
7. Implicit multiplication before constants/variables: $2\pi$, $3A$, $2\sqrt{3}$.
8. Permutations and Combinations: $n\text{P}r, n\text{C}r$.
9. Implicit multiplication before parentheses: $2(3)$.
10. Explicit multiplication and division: $\times, \div$.
11. Addition and subtraction: $+ , -$.
12. Relational equality/assignments: $=, :$.

**Special Parser Features:**
- **Auto-closing Parentheses:** If an expression ends with open parentheses when `=` is pressed, the parser automatically inserts matching closing parentheses (e.g., `sin(30` parses as `sin(30)`).
- **Multi-statement support (`:`):** Parses expressions separated by `:`, allowing sequential evaluation on repeated `=` presses.

**Acceptance Criteria:**
- Correctly parses complex chained operations respecting precedence.
- Auto-closes trailing open parentheses.
- Emits structured `SyntaxError` with precise character position on malformed syntax.

---

### Step 3 — Core Evaluator & Exact Arithmetic (SymPy Integration)

**Target Files:**
- `src/core/math/evaluator.py`
- `src/core/math/formatter.py`
- `test/test_evaluator.py`
- `test/test_fractions_powers.py`

**Design Specifications:**
1. **Exact Representation Engine:**
   - Uses SymPy `Rational` for rational arithmetic: $\frac{1}{2} + \frac{1}{3} = \frac{5}{6}$.
   - Exact radical simplification: $\sqrt{12} \rightarrow 2\sqrt{3}$, $\sqrt{2} + \sqrt{8} \rightarrow 3\sqrt{2}$.
   - Exact trigonometric results in standard angles: $\sin(30^\circ) \rightarrow \frac{1}{2}$, $\cos(45^\circ) \rightarrow \frac{\sqrt{2}}{2}$, $\tan(60^\circ) \rightarrow \sqrt{3}$.
   - Exact $\pi$ scaling: expressions with $\pi$ retain exact $\pi$ multipliers in MthIO mode.
2. **Operations Supported:**
   - Addition, subtraction, multiplication, division.
   - Fractions: simple proper/improper $\frac{a}{b}$, mixed $a\frac{b}{c}$.
   - Powers: $x^2, x^3, x^y$, $10^x, e^x$.
   - Roots: $\sqrt{x}, \sqrt[3]{x}, \sqrt[y]{x}$.
   - Reciprocal: $x^{-1} = \frac{1}{x}$.
   - Factorial: $n!$ for non-negative integers $n \le 69$. ($n \ge 70$ or non-integer triggers `Math ERROR`).
   - Percentage: $A + B\%$ evaluates to $A \times (1 + B/100)$; $A \times B\%$ evaluates to $A \times B / 100$.
3. **Execution Safety:**
   - Prevent unbounded computation timeouts with strict step/time limits.
   - Maximum result magnitude: $10^{100}$ (overflow triggers `Math ERROR`).

**Acceptance Criteria:**
- Accurate exact results for rational and radical expressions in MthIO.
- Seamless decimal fallback in LineIO or when exact form is not closed.
- Factorials, powers, and roots produce exact answers within standard domains.

---

### Step 4 — Scientific Functions & Angle Systems

**Target Files:**
- `src/core/math/evaluator.py` (extensions)
- `test/test_trig_log.py`

**Design Specifications:**
1. **Angle Modes:**
   - `DEG` (Degrees): $\pi \text{ rad} = 180^\circ$.
   - `RAD` (Radians): native radian calculus.
   - `GRA` (Gradians): $\pi \text{ rad} = 200 \text{ grad}$.
   - Input angle conversions: override current angle unit using explicit angle symbols ($^\circ, ^r, ^g$).
2. **Trigonometric & Inverse Trigonometric Functions:**
   - $\sin(x), \cos(x), \tan(x)$. Handling singularities: $\tan(90^\circ) \rightarrow \text{Math ERROR}$.
   - $\sin^{-1}(x), \cos^{-1}(x), \tan^{-1}(x)$. Domain checking: $|x| \le 1$ for $\sin^{-1}, \cos^{-1}$.
3. **Hyperbolic & Inverse Hyperbolic Functions:**
   - $\sinh(x), \cosh(x), \tanh(x)$.
   - $\sinh^{-1}(x), \cosh^{-1}(x), \tanh^{-1}(x)$. Domain checking: $x \ge 1$ for $\cosh^{-1}$.
4. **Logarithms & Exponentials:**
   - Natural $\ln(x)$ and $e^x$.
   - Common $\log(x)$ (base 10) and $10^x$.
   - Arbitrary base $\log_a(b)$ (accessible via Casio $\log_{\square}(\square)$ key).
   - Domain checking: $x > 0$ for logarithms; $a > 0, a \ne 1$ for base $a$.
5. **Combinatorics & Random Functions:**
   - Permutations: $n\text{P}r = \frac{n!}{(n-r)!}$ ($0 \le r \le n$, integers).
   - Combinations: $n\text{C}r = \frac{n!}{r!(n-r)!}$ ($0 \le r \le n$, integers).
   - Random Number $\text{Ran}\#$: generates pseudo-random 3-decimal fraction in $[0.000, 0.999]$.
   - Random Integer $\text{RanInt}\#(a, b)$: generates random integer in $[a, b]$ where $a \le b$.
   - Rounding $\text{Rnd}(x)$: rounds value to match current display format (Fix/Sci).
   - Absolute value: $\text{Abs}(x) = |x|$.

**Acceptance Criteria:**
- Accurate evaluations across all 3 angle modes.
- Precise domain checks throwing `Math ERROR` on mathematical violations.
- Standard Casio combinatorics and random generation behavior.

---

### Step 5 — Natural Textbook Display (MthIO) & Cursor Navigation

**Target Files:**
- `src/ui/natural_canvas.py`
- `src/ui/calculator_display.py`
- `src/core/math/ast_nodes.py`
- `test/test_display_natural.py`

**Design Specifications:**
1. **Natural Textbook Display Architecture:**
   - Support both `MthIO` (MathO / LineO) and `LineIO`.
   - In `MthIO-MathO`: expressions and results render in 2D textbook format:
     - Vertical stacked fractions: $\frac{\text{num}}{\text{den}}$ with horizontal division bar.
     - Radicals: $\sqrt{\text{radicand}}$ with top vinculum bar and index notch for $\sqrt[n]{x}$.
     - Superscript exponents: $x^2$, $x^y$.
     - Large calculus symbols: $\int_{a}^{b} f(x)dx$ and $\sum_{x=a}^{b} f(x)$ with upper/lower bounds.
2. **2D Cursor & Navigation Model:**
   - The cursor can enter nested slots:
     - Inside numerator $\leftrightarrow$ press ▼ to jump to denominator.
     - Inside denominator $\leftrightarrow$ press ▲ to jump to numerator.
     - Press ▶ at the end of denominator/numerator to exit the fraction.
     - Inside exponent $\leftrightarrow$ press ▶ to step down to baseline.
     - Inside radical $\leftrightarrow$ press ▶ to exit under the radical bar.
3. **Rendering Implementation:**
   - Implement `NaturalCanvas` using PySide6 `QPainter` / font metrics or styled layout blocks, ensuring crisp LCD-style presentation matching the calculator's visual theme (#17271f on #cbdac7).
   - Maintain full fallback to 1D linear string editing in `LineIO` mode.

**Acceptance Criteria:**
- 2D mathematical structures render clearly with correct proportional scaling.
- Arrow keys (◀, ▶, ▲, ▼) traverse nested 2D mathematical slots smoothly.
- Backspace / DEL removes elements hierarchically without corrupting the expression tree.

---

### Step 6 — Formatting, S⇔D Switching, and Engineering Notation

**Target Files:**
- `src/core/math/formatter.py`
- `src/core/state.py`
- `test/test_formatting.py`

**Design Specifications:**
1. **Exact ⇔ Decimal Switching (`S⇔D`):**
   - The user can press `S⇔D` after evaluation to toggle between:
     - Exact fraction $\leftrightarrow$ Decimal ($\frac{1}{4} \leftrightarrow 0.25$).
     - Exact radical $\leftrightarrow$ Decimal ($\sqrt{2} \leftrightarrow 1.414213562$).
     - Exact $\pi$ expression $\leftrightarrow$ Decimal ($\pi \leftrightarrow 3.141592654$).
     - Mixed fraction $\leftrightarrow$ Improper fraction via SHIFT + `S⇔D` ($1\frac{1}{2} \leftrightarrow \frac{3}{2}$).
2. **Number Display Formats:**
   - `Fix 0–9`: fixed number of decimal places with rounding.
   - `Sci 0–9`: scientific notation with specified significant figures ($1.234 \times 10^3$).
   - `Norm 1`: exponential format if $|x| < 10^{-2}$ or $|x| \ge 10^{10}$; otherwise decimal.
   - `Norm 2`: exponential format if $|x| < 10^{-9}$ or $|x| \ge 10^{10}$; otherwise decimal (default).
3. **Engineering Notation (`ENG`):**
   - Pressing `ENG` converts exponent to a multiple of 3 ($10^3, 10^6, 10^{-3}$, etc.).
   - Subsequent `ENG` presses shift exponent down by 3 (multiplying mantissa by 1000).
   - SHIFT + `ENG` ($\leftarrow$) shifts exponent up by 3 (dividing mantissa by 1000).

**Acceptance Criteria:**
- `S⇔D` cycles through all applicable exact, improper, mixed, and decimal representations.
- Fix, Sci, and Norm format numbers accurately with rounding according to setup.
- `ENG` and SHIFT+`ENG` adjust exponents by multiples of 3 correctly.

---

### Step 7 — Memory Systems, Variables, and Replay History

**Target Files:**
- `src/core/math/memory.py`
- `src/core/state.py`
- `src/core/controller.py`
- `test/test_memory.py`
- `test/test_replay.py`

**Design Specifications:**
1. **Memory Registers:**
   - `Ans`: Automatically stores the evaluated result of the last calculation.
   - `PreAns`: Stores the previous answer prior to the last calculation.
   - Independent Memory `M`:
     - `M+`: adds current expression result to `M`.
     - SHIFT + `M+` (`M−`): subtracts current expression result to `M`.
     - When $M \ne 0$, the `M` indicator illuminates on the LCD.
   - General Variables: $A, B, C, D, E, F, X, Y$.
   - `STO` + [Variable]: stores current result or input into target variable.
   - `RCL` + [Variable]: recalls variable value onto the input line or displays value.
   - Clear Memory: SHIFT + `9` (`CLR`) menu:
     - `1: Setup` $\rightarrow$ resets setup to defaults.
     - `2: Memory` $\rightarrow$ clears variables $A-F, X, Y, M$, Ans, PreAns.
     - `3: All` $\rightarrow$ resets setup and clears all memory.
2. **Calculation History & Replay:**
   - Circular history buffer storing the last 30 calculations (expression + result).
   - Pressing ▲ / ▼ scrolls through previous calculations.
   - Pressing ◀ or ▶ when viewing a historical calculation copies that expression into the active editor for editing.
   - Consecutive operator entry: pressing an operator (`+`, `-`, `×`, `÷`, `^`) when the input line is empty automatically inserts `Ans` as the first operand.

**Acceptance Criteria:**
- Memory variables preserve values across evaluations until explicitly overwritten or cleared.
- Replay buffer allows historical inspection and editable recall.
- `Ans` auto-insertion functions seamlessly for continuous chaining.

---

### Step 8 — Remaining COMP Operations (Calculus, Coordinates, DMS, CALC, SOLVE)

**Target Files:**
- `src/core/math/calculus.py`
- `src/core/math/coordinates.py`
- `src/core/math/solver.py`
- `test/test_calculus.py`
- `test/test_coordinates_dms.py`
- `test/test_solve_calc.py`

**Design Specifications:**
1. **Coordinate Conversion:**
   - Rectangular to Polar: $\text{Pol}(x, y) \rightarrow r = \sqrt{x^2+y^2}, \theta = \text{atan2}(y, x)$. Displays $r$ and $\theta$, stores $r \rightarrow X$, $\theta \rightarrow Y$.
   - Polar to Rectangular: $\text{Rec}(r, \theta) \rightarrow x = r\cos(\theta), y = r\sin(\theta)$. Displays $x$ and $y$, stores $x \rightarrow X$, $y \rightarrow Y$.
2. **Sexagesimal DMS ($^\circ\ '\ ''$):**
   - Input format: degrees, minutes, seconds using `° ' "` key (e.g. `2°20°30°`).
   - Conversion: pressing `° ' "` after calculation converts decimal result to DMS (e.g. $2.341666667 \rightarrow 2^\circ 20^\circ 30^\circ$).
3. **Numerical Calculus:**
   - Numerical Derivative: $\left.\frac{d}{dx}f(x)\right|_{x=a}$ evaluated using central difference approximation with adaptive step size $\Delta x$, or exact SymPy derivative evaluation when symbolic.
   - Numerical Integration: $\int_{a}^{b} f(x) dx$ using Gauss-Kronrod quadrature or Simpson's rule, respecting angle settings for trigonometric integrands.
   - Summation: $\sum_{x=a}^{b} f(x)$ evaluated for integer limits $a \le b$.
4. **Interactive Commands:**
   - **`CALC`:**
     - Evaluates expressions containing variables ($A, B, C, D, E, F, X, Y$).
     - Pressing `CALC` prompts user for values of each variable sequentially (`X?`, `Y?`), showing current value as default.
     - Pressing `=` computes result without modifying the original expression.
   - **`SOLVE`:**
     - Solves equations in the form $f(X) = 0$ or $f(X) = g(X)$ for variable $X$.
     - Prompts for initial estimate (`X?`).
     - Solves using Newton-Raphson method with Secant fallback.
     - Displays solution:
       ```text
       X = [value]
       L - R = [residual]
       ```
     - Displays `Can't Solve` if the algorithm fails to converge within iteration limit.

**Acceptance Criteria:**
- $\text{Pol}$ and $\text{Rec}$ store results in $X$ and $Y$ variables as documented.
- DMS values convert bidirectionally without precision drift.
- Numerical integration and differentiation match official Casio manual tolerance.
- `CALC` and `SOLVE` interactive prompts operate smoothly with full UI feedback.

---

### Step 9 — Diagnostic Error Handling & Jump-to-Error

**Target Files:**
- `src/core/math/errors.py`
- `src/core/controller.py`
- `src/ui/calculator_display.py`
- `test/test_errors.py`

**Design Specifications:**
1. **Casio Error Categories:**
   - `Math ERROR`: Zero division, domain violations, overflow ($> 9.999999999 \times 10^{99}$), factorial of negative or non-integer.
   - `Syntax ERROR`: Invalid operator placement, unclosed structures, misplaced commas or colons.
   - `Stack ERROR`: Expression complexity exceeds calculation stack limit.
   - `Argument ERROR`: Invalid function arguments (e.g., negative random bounds, $r > n$ in $n\text{P}r$).
   - `Can't Solve`: SOLVE fails to locate a root.
2. **Error Screen Interaction:**
   - When an error occurs, the LCD displays:
     ```text
     [Error Name]
     [AC]   :Cancel
     [◀][▶] :Goto
     ```
   - Pressing `AC`: Clears the error screen and clears the expression buffer.
   - Pressing `◀` or `▶`: Clears the error screen, restores the expression, and positions the cursor directly at the location where the error originated.

**Acceptance Criteria:**
- Accurate error classification for all error conditions.
- `Goto` cursor positioning matches the exact failure locus in the expression.

---

### Step 10 — Controller Integration & Key Registry Finalization

**Target Files:**
- `src/core/key_registry.py`
- `src/core/controller.py`
- `src/core/action.py`
- `test/test_controller.py`
- `test/test_comp_manual.py`

**Design Specifications:**
1. Upgrade all remaining `Kind.DEFERRED` actions associated with COMP mode in `REGISTRY` to active operational actions:
   - Primary: `fraction`, `sqrt`, `square`, `power`, `log`, `ln`, `hyp`, `sin`, `cos`, `tan`, `rcl`, `eng`, `sd`, `mplus`, `ans`, `factorial`, `equals`, `reciprocal`, `random`.
   - Shift: `solve`, `derivative`, `mixed_fraction`, `cube_root`, `cube`, `nth_root`, `ten_power`, `exp`, `arg`, `arrow_dms`, `inv_hyp`, `asin`, `acos`, `atan`, `sto`, `arrow_eng`, `abs`, `mixed_sd`, `mminus`, `const`, `conv`, `clr`, `pol`, `rec`, `npr`, `ncr`, `rnd`, `ranint`.
   - Alpha: `equals` (`=`), colon (`:`), variable letters $A, B, C, D, E, F, X, Y, M$, constant $e$, `preans`.
2. Controller handles full calculation lifecycle:
   - Pressing `=` evaluates the expression and enters result display state.
   - Pressing numbers or functions after evaluation starts a fresh expression.
   - Pressing operators (`+`, `-`, etc.) after evaluation chains `Ans` to the new operation.

**Acceptance Criteria:**
- Zero deferred actions remain for any COMP mode key or modifier.
- All manual and keyboard shortcuts invoke the integrated calculation pipeline.

---

## 4. Verification Matrix & Manual Test Scenarios

The following validation suite mirrors the official Casio fx-570ES PLUS User's Guide (COMP mode chapters):

| Scenario | Input Sequence | Expected Output (MthIO) | Expected Output (LineIO) |
|---|---|---|---|
| Basic Arithmetic | `3 + 5 × 2 =` | `13` | `13` |
| Negative Number | `(−) 5 + 2 =` | `-3` | `-3` |
| Fraction Addition | `1 □/□ 2 + 1 □/□ 3 =` | `5/6` | `5/6` |
| Mixed Fraction | `SHIFT ■□/□ 1 2 3 + 1 □/□ 2 =` | `13/6` | `13/6` |
| S⇔D Toggle | Press `S⇔D` on `5/6` | `0.8333333333` | `0.8333333333` |
| Square Root Simplification | `√ 12 =` | `2√3` | `3.464101615` |
| Trigonometry (DEG) | `sin 30 =` | `1/2` | `0.5` |
| Trigonometry (RAD) | `SETUP RAD`, `sin ( π ÷ 6 ) =` | `1/2` | `0.5` |
| Factorial | `5 SHIFT x! =` | `120` | `120` |
| Permutations & Combinations | `5 SHIFT nPr 2 =`, `5 SHIFT nCr 2 =` | `20`, `10` | `20`, `10` |
| Powers of 10 & ENG | `12345 =`, press `ENG` | `12.345×10³` | `12.345×10³` |
| Variable Storage & Recall | `12 SHIFT STO A`, `ALPHA A × 2 =` | `24` | `24` |
| Ans Memory Chaining | `2 + 3 =`, `+ 4 =` | `Ans + 4` $\rightarrow$ `9` | `Ans + 4` $\rightarrow$ `9` |
| Polar Conversion | `SHIFT Pol 1 , 1 =` | `r=1.414213562, θ=45` | `r=1.414213562, θ=45` |
| Sexagesimal DMS | `2 °'″ 20 °'″ 30 °'″ + 39 °'″ 30 °'″ =` | `3°00°00°` | `3°00°00°` |
| Numerical Derivative | `SHIFT d/dx ( X ^ 2 , 3 ) =` | `6` | `6` |
| Numerical Integration | `∫ ( X ^ 2 , 0 , 3 ) =` | `9` | `9` |
| Discrete Summation | `SHIFT Σ ( X , 1 , 10 ) =` | `55` | `55` |
| SOLVE Equation | `X ^ 2 = 4`, `SHIFT SOLVE`, `0 =` | `X=2, L-R=0` | `X=2, L-R=0` |
| Error Goto | `5 ÷ 0 =`, press `◀` | Cursor at `0` | Cursor at `0` |

---

## 5. Definition of Done for Phase 2

Phase 2 is strictly complete when:

1. **All COMP Operations Implemented:** Every documented COMP mode mathematical operation is fully functional without mocks or placeholders.
2. **Natural Display Parity:** Natural Textbook Display (2D fractions, roots, powers, integrals) renders accurately and supports cursor editing.
3. **Exact & Decimal Switching:** `S⇔D` operates seamlessly across all supported exact mathematical forms and decimal approximations.
4. **Memory & History Active:** Variables $A-F, X, Y, M$, `Ans`, `PreAns`, and calculation history replay function with 100% adherence to calculator behavior.
5. **Robust Error Handling:** All mathematical and syntax errors display proper Casio-style diagnostic screens with working `Goto` cursor positioning.
6. **Automated Test Coverage:**
   - 100% pass rate across all new and existing unit, integration, and manual verification tests.
   - Zero test regressions from Phase 1.
7. **Task Tracking:** `TASKS.md` Phase 2 checkboxes are checked off only after all implementations and test suites pass verification.
