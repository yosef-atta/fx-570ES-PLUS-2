# Casio fx-570ES PLUS 2nd Edition — Native Windows Scientific Calculator

[![Tests](https://img.shields.io/badge/tests-195%20passed-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

A complete, free, offline native Windows desktop scientific calculator replicating the physical **Casio fx-570ES PLUS 2nd Edition** to the millimeter in both look, behavior, mathematical capabilities, and hardware ergonomics.

---

## Features

### 1. Authentic 1:1 Physical Casio Design
* **Matte Black Casing:** Rounded rectangle body (`border-radius: 36px`) in authentic graphite/charcoal casing (#18191C).
* **Authentic Branding:** Official `CASIO`, `fx-570ES PLUS`, `NATURAL-V.P.A.M.`, and `2nd edition` headers.
* **Greenish-Gray LCD:** Recessed bezel housing with dot-matrix LCD background (#C2CEB8) and dark charcoal pixels.
* **Circular REPLAY D-Pad:** Analog metallic styling with central `REPLAY` hub and 4-way arrow clickers (`▲`, `▼`, `◀`, `▶`).
* **Vibrant Lime Green Keys:** Signature Casio `DEL` and `AC` buttons (#7DAE2E) with gold sub-labels `INS` and `OFF`.
* **Oval Control Keys:** Metallic oval buttons for `SHIFT`, `ALPHA`, `MODE`, and `ON`.

### 2. All 8 Calculator Modes
1. **COMP (Mode 1):** General arithmetic, trigonometry, hyperbolics, logarithms, fractions, coordinate conversions (`Pol`/`Rec`), DMS, numerical calculus ($\frac{d}{dx}$, $\int$), summation ($\sum$), `CALC`, `SOLVE`, and recurring decimal conversion (.0121111 $\to$ $\frac{109}{9000}$).
2. **CMPLX (Mode 2):** Complex numbers ($a+bi$ and polar $r\angle\theta$), `arg(z)`, `Conjg(z)`.
3. **STAT (Mode 3):** Single-variable data entry, 7 regression models ($A+BX$, $A+BX+CX^2$, $\ln X$, $e^X$, $A\cdot B^X$, $A\cdot X^B$, $1/X$), summation metrics, and normal distributions ($P, Q, R, \blacktriangleright t$).
4. **BASE-N (Mode 4):** Binary, Octal, Decimal, Hexadecimal representation with bitwise logic (`and`, `or`, `xor`, `xnor`, `Not`, `Neg`).
5. **EQN (Mode 5):** 2-unknown & 3-unknown simultaneous linear equations, quadratic polynomials ($aX^2+bX+c=0$), and cubic polynomials ($aX^3+bX^2+cX+d=0$) with complex roots.
6. **MATRIX (Mode 6):** 3 matrices (MatA, MatB, MatC) up to $3\times3$, determinants (`det`), matrix inversion ($M^{-1}$), transposition (`Trn`), and arithmetic.
7. **TABLE (Mode 7):** Simultaneous tabular evaluation for $f(x)$ and $g(x)$ across user-defined Start, End, and Step ranges.
8. **VECTOR (Mode 8):** 3 vectors (VctA, VctB, VctC) in 2D or 3D, dot product (`Dot`), cross product ($\times$), and magnitudes.
9. **Constants & Conversions:** All 40 built-in scientific constants (`CONST 01~40`) and 40 metric conversions (`CONV 01~40`).

### 3. Natural Textbook Display & Buffer Controls
* **2D Stacked Fractions:** Exact horizontal fraction bars ($\frac{\text{Numerator}}{\text{Denominator}}$) in MthIO mode.
* **99-Character Capacity:** Strict 99-character input capacity matching the physical hardware.
* **Hardware Warning Cursor:** Automatically switches from vertical line `│` to solid block `■` when $\le 10$ bytes remain ($\ge 89$ characters), matching the official Casio manual.
* **Full Indicator & Audio Alert:** Displays `FULL` on the LCD status bar when capacity is reached and sounds an audible beep upon typing attempts beyond the limit.
* **Horizontal Scrolling:** Smooth sliding viewport with `◀` and `▶` indicators, plus `Home` and `End` instant jump keys.

### 4. Settings Persistence & Custom Shortcuts
* **Persistent Settings:** Automatically saves angle unit, number formats (`Norm`, `Fix`, `Sci`), display formats (`MthIO`, `LineIO`), and window geometry across sessions.
* **Configurable Shortcuts:** Support for custom keyboard mapping in `src/input/keyboard.py`.

---

## Keyboard Shortcuts Reference

| Keyboard Key | Calculator Function | Description |
|---|---|---|
| `0` – `9` | `0` – `9` | Numeric digits |
| `+`, `-`, `*`, `/` | `+`, `−`, `×`, `÷` | Arithmetic operators |
| `Enter` / `Return` / `=` | `=` | Evaluate expression |
| `Backspace` / `Delete` | `DEL` | Delete character at cursor |
| `Escape` | `AC` | All Clear / cancel menu |
| `Left` / `Right` ($\leftarrow$ / $\rightarrow$) | `◀` / `▶` | Move cursor / scroll expression |
| `Up` / `Down` ($\uparrow$ / $\downarrow$) | `▲` / `▼` | History navigation / menu pages |
| `Home` | `Home` | Jump instantly to beginning of expression |
| `End` | `End` | Jump instantly to end of expression |
| `F2` | `SHIFT` | Toggle Shift modifier (Gold) |
| `F3` | `ALPHA` | Toggle Alpha modifier (Pink) |
| `F4` | `MODE` | Open Mode selection menu |
| `F5` | `SETUP` | Open Setup configuration menu |
| `s` | `sin` | Sine function |
| `c` | `cos` | Cosine function |
| `t` | `tan` | Tangent function |
| `l` | `ln` | Natural logarithm |
| `r` | `√` | Square root |
| `!` | `x!` | Factorial |
| `i` | `i` | Imaginary unit ($i$) |
| `p` | `π` | Mathematical constant $\pi$ |
| `^` | `x^` | Exponentiation |
| `(` / `)` | `(` / `)` | Parentheses |

---

## Running the Application

### Option 1: Standalone Windows Executable (No Python Required)
1. Download or locate `dist/Casio-fx570ES-PLUS-2/Casio-fx570ES-PLUS-2.exe`.
2. Double-click `Casio-fx570ES-PLUS-2.exe` to run immediately.

### Option 2: Running from Source
Ensure Python 3.10+ is installed:
```bash
# Clone the repository
git clone https://github.com/yosef-atta/fx-570ES-PLUS-2.git
cd fx-570ES-PLUS-2

# Run using uv
uv run python -m src.app

# Or using standard python
python -m src.app
```

---

## Building the Windows Executable

To compile a standalone distribution package using PyInstaller:
```bash
uv run python scripts/build_windows.py
```
The output will be placed in `dist/Casio-fx570ES-PLUS-2/`.

---

## Running the Automated Test Suite

All 195 automated tests can be verified using `pytest`:
```bash
uv run pytest
```
