# PHASE-1.md — Application Foundation

**Project:** Scientific Calculator — fx-570ES PLUS-2 Inspired  
**Phase:** 1 — Application Foundation  
**Status:** Not Started  
**Target:** Windows 10/11  
**Python:** 3.10.11  
**Dependencies:** PySide6, SymPy, pytest, uv

---

## 1. Objective

Build a working native Windows scientific calculator interface inspired by the Casio fx-570ES PLUS-2 (2nd Edition).

Phase 1 establishes the application structure, calculator layout, display, input handling, state management, and interaction system.

All physical calculator keys must be represented and mapped to the correct actions. Implemented foundation interactions must work through both mouse and keyboard input.

Mathematical evaluation, natural mathematical expression rendering, and advanced calculator modes belong to later phases.

### Phase 1 completion requirements

- The application launches successfully on Windows.
- The calculator window renders with the complete physical key layout.
- All keys have registered actions and correct modifier mappings.
- Mouse and keyboard input use the same action-dispatch system.
- SHIFT, ALPHA, DEL, AC, MODE, and SETUP interactions work.
- Cursor movement and menu navigation work.
- Display state updates correctly.
- Foundation tests pass.

**Important:** A registered action does not imply its mathematical operation has been implemented. Phase 1 must not produce fabricated calculation results or silently treat unsupported operations as successful.

---

## 2. Architecture

Use the following project structure:

~~~text
fx-570ES-PLUS-2/
│
├── pyproject.toml
├── uv.lock
├── .python-version
├── TASKS.md
│
├── src/
│   ├── app.py
│   │
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── calculator_display.py
│   │   ├── calculator_key.py
│   │   ├── keypad.py
│   │   ├── menu_view.py
│   │   └── style.py
│   │
│   ├── core/
│   │   ├── action.py
│   │   ├── state.py
│   │   ├── controller.py
│   │   └── key_registry.py
│   │
│   └── input/
│       └── keyboard.py
│
├── test/
│   ├── conftest.py
│   ├── test_launch.py
│   ├── test_key_registry.py
│   ├── test_keypad.py
│   ├── test_display.py
│   ├── test_keyboard.py
│   ├── test_state.py
│   ├── test_controller.py
│   └── test_menu.py
│
├── asset/
│   └── icons/
│
└── plan/
    ├── PHASE-1.md
    ├── PHASE-2.md
    ├── PHASE-3.md
    ├── PHASE-4.md
    └── PHASE-5.md
~~~

Standard Python package initialization files may be added during implementation without documenting them individually.

### Architecture responsibilities

| Component | Responsibility |
|---|---|
| `app.py` | Application startup and dependency wiring |
| `ui/` | Visual components and Qt interaction |
| `core/` | Actions, calculator state, registry, and controller |
| `input/` | Keyboard-to-calculator input mapping |
| `test/` | Automated foundation tests |
| `asset/` | Local application assets |
| `plan/` | Phase implementation documentation |

### Dependency direction

~~~text
Mouse Input ────────┐
                    │
Keyboard Input ─────┤
                    ▼
              Action Registry
                    │
                    ▼
                Controller
                    │
                    ▼
              Calculator State
                    │
                    ▼
              UI State Refresh
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
        Display              Menus
~~~

Architecture rules:

1. UI components never implement mathematical calculations.
2. Keyboard handling never modifies calculator state directly.
3. All calculator actions pass through the controller.
4. The action registry is the authoritative source for physical key definitions.
5. The controller manages state transitions.
6. State objects do not depend on PySide6.
7. Qt widgets render state and forward user input.
8. Avoid circular imports and duplicated action mapping.
9. No additional architectural layers unless an actual requirement justifies them.

---

## 3. Implementation Steps

### Step 1 — Application Entry Point

**Files:**
- `src/app.py`
- `src/ui/main_window.py`
- `test/test_launch.py`

Tasks:

- [ ] Create the PySide6 application entry point.
- [ ] Initialize `QApplication`.
- [ ] Instantiate the calculator controller and initial state.
- [ ] Create and show the main calculator window.
- [ ] Connect controller updates to the window.
- [ ] Configure the application name and basic metadata.
- [ ] Ensure application startup does not execute mathematical operations.
- [ ] Support clean application shutdown.
- [ ] Add launch and shutdown tests.

Entry-point responsibility:

~~~text
app.py
  ├── Create QApplication
  ├── Create CalculatorState
  ├── Create Controller
  ├── Create MainWindow
  ├── Connect actions and state updates
  ├── Show window
  └── Start Qt event loop
~~~

**Acceptance criteria:** The application opens a visible native window and exits cleanly without exceptions.

### Step 2 — Action Definitions and Key Registry

**Files:**
- `src/core/action.py`
- `src/core/key_registry.py`
- `test/test_key_registry.py`

Create a typed action system covering calculator input and interactions.

Action categories:

| Category | Examples |
|---|---|
| Numeric | 0–9, decimal point |
| Arithmetic | +, −, ×, ÷ |
| Expression | Parentheses, powers, fractions, roots |
| Scientific | sin, cos, tan, log, ln |
| Editing | DEL, AC, cursor movement |
| Modifiers | SHIFT, ALPHA |
| Menus | MODE, SETUP, selection |
| Evaluation | =, S⇔D, CALC, SOLVE |
| Memory | STO, RCL, Ans |
| System | ON, OFF |

Define immutable action records containing:

- Action identifier
- Action category
- Optional payload
- Source physical key identifier

Define immutable physical key specifications containing:

- Unique physical key ID
- Primary label/action
- SHIFT label/action, if present
- ALPHA label/action, if present
- Calculator layout position
- Visual key category

The registry must cover every physical key shown in the reference layout, including alternate functions.

Use stable identifiers independent of visible labels. For example, a key labelled `sin` can dispatch either the sine action or inverse-sine action depending on modifier state.

**Modifier priority:** Resolve primary, SHIFT, and ALPHA mappings centrally. Treat SHIFT and ALPHA as mutually exclusive selection modifiers unless manual verification establishes an exception for a particular operation.

Tasks:

- [ ] Define action types and IDs.
- [ ] Define the physical key registry.
- [ ] Register primary functions for every key.
- [ ] Register all documented SHIFT and ALPHA functions.
- [ ] Represent mode-specific alternatives without duplicating physical buttons.
- [ ] Implement key/action lookup.
- [ ] Reject duplicate physical key IDs and invalid action definitions.
- [ ] Add registry completeness and mapping tests.

**Acceptance criteria:** Every rendered physical key resolves to a valid action definition under its supported modifiers. Mathematical actions not yet implemented remain explicitly deferred.

### Step 3 — Calculator State

**Files:**
- `src/core/state.py`
- `test/test_state.py`

Create a small, deterministic calculator state model.

Required state:

| State field | Purpose | Initial value |
|---|---|---|
| `expression` | Current linear input buffer | Empty |
| `cursor_position` | Cursor position within input | 0 |
| `result` | Displayed result | Empty |
| `mode` | Current calculation mode | COMP |
| `shift_active` | SHIFT indicator | False |
| `alpha_active` | ALPHA indicator | False |
| `active_menu` | Open calculator menu | None |
| `menu_page` | Active menu page | 0 |
| `angle_unit` | Angle measurement setting | DEG |
| `display_format` | Mathematical display setting | MthIO-MathO |
| `number_format` | Number display setting | Norm 1 |
| `input_mode` | Input editing behavior | Insert |
| `power_on` | Calculator power state | True |

Maintain a separate focused menu selection value if needed for keyboard navigation.

Use a small enum or equivalent constrained values for modes and settings.

Tasks:

- [ ] Implement default state initialization.
- [ ] Implement cursor bounds validation.
- [ ] Implement modifier state behavior.
- [ ] Implement menu state transitions.
- [ ] Implement mode and setup state storage.
- [ ] Implement reset behavior for Phase 1-owned state.
- [ ] Keep state independent of Qt widgets.
- [ ] Add state initialization and transition tests.

State must be the source of truth. Widgets must not maintain competing copies of calculator mode, modifiers, or expression content.

**Acceptance criteria:** State transitions are deterministic, valid, and independently testable.

### Step 4 — Controller and Action Dispatch

**Files:**
- `src/core/controller.py`
- `test/test_controller.py`

Implement the controller as the central interaction coordinator.

Main responsibility:

~~~text
Receive Action
      ↓
Resolve Active Modifier / Context
      ↓
Determine Required State Transition
      ↓
Update Calculator State
      ↓
Notify UI
~~~

Required controller behaviors:

**Numeric input**
- Insert digits at the current cursor position.
- Insert decimal points as input tokens.
- Update cursor position.
- Preserve input order.

**Editing**
- DEL removes the token before the cursor.
- AC clears the current expression and result.
- Left/right arrows move the expression cursor.
- Cursor positions remain within valid bounds.

**SHIFT**
- Activates SHIFT modifier.
- Updates display indicator.
- Resolves the next applicable key using its shifted mapping.
- Clears the one-shot modifier after the appropriate action.

**ALPHA**
- Activates ALPHA modifier.
- Updates display indicator.
- Resolves the next applicable key using its alphabetic mapping.
- Clears the one-shot modifier after the appropriate action.

**MODE**
- Opens calculation mode selection.
- Allows choosing any of the eight documented modes.
- Updates current mode.
- Closes the menu after selection.

**SETUP**
- SHIFT + MODE opens the calculator setup menu.
- Shows supported setup options.
- Accepts numeric selection and navigation actions.
- Updates the relevant settings.

**Menu behavior**
- AC cancels an open menu.
- Numeric selection executes the corresponding menu command.
- Arrow keys navigate menu pages or selections as appropriate.
- Invalid selections do not corrupt state.

**Power**
- ON activates the calculator.
- SHIFT + AC dispatches OFF.
- Power-off disables normal input until ON is pressed.

Tasks:

- [ ] Implement central action dispatch.
- [ ] Implement numeric input and basic editing.
- [ ] Implement SHIFT and ALPHA resolution.
- [ ] Implement MODE and SETUP routing.
- [ ] Implement menu selection and cancellation.
- [ ] Implement cursor movement.
- [ ] Implement power state transitions.
- [ ] Expose state-change notifications to the UI.
- [ ] Add controller transition tests.

Calculation-specific actions may be recognized without execution during Phase 1. They must never display an invented result.

**Acceptance criteria:** Every foundation interaction produces the correct observable state transition.

### Step 5 — Main Window and Styling

**Files:**
- `src/ui/main_window.py`
- `src/ui/style.py`

Build the calculator as a standalone desktop window with an original visual identity inspired by the reference hardware.

Design goals:

- Familiar fx-570ES PLUS-2 key organization.
- Compact calculator proportions.
- Clear visual hierarchy between navigation, scientific, and arithmetic keys.
- Distinct SHIFT and ALPHA labeling.
- High-contrast readable display.
- Consistent borders, spacing, typography, and interaction feedback.

Avoid copying official branding, trademarks, and decorative assets directly.

Tasks:

- [ ] Create the main window.
- [ ] Create the main calculator shell layout.
- [ ] Reserve space for display and indicators.
- [ ] Reserve space for the complete physical keypad.
- [ ] Define consistent colors and typography.
- [ ] Define key sizing and layout spacing.
- [ ] Configure minimum window size.
- [ ] Ensure resizing does not clip or overlap keys.
- [ ] Add active, pressed, and disabled visual states.
- [ ] Add appropriate keyboard focus behavior.

Use Qt layouts rather than absolute positioning wherever practical. Key positions should be controlled by the keypad layout model.

**Acceptance criteria:** All controls are visible, properly aligned, readable, and usable on the targeted Windows display environment.

### Step 6 — Calculator Key and Keypad

**Files:**
- `src/ui/calculator_key.py`
- `src/ui/keypad.py`
- `test/test_keypad.py`

Create one reusable button component for calculator keys.

Each key displays:

- Primary label
- Optional SHIFT label
- Optional ALPHA label
- Appropriate color and visual category

The button emits its physical key identifier on click.

The keypad uses the key registry to construct the complete layout.

Tasks:

- [ ] Implement reusable calculator key widget.
- [ ] Implement primary and alternate key labels.
- [ ] Implement button hover, press, and focus feedback.
- [ ] Build the physical key layout from registry definitions.
- [ ] Include the four-direction navigation control.
- [ ] Connect every button to the central input dispatcher.
- [ ] Preserve consistent button dimensions.
- [ ] Avoid duplicate widget-specific action logic.
- [ ] Test physical key coverage and dispatch.

**Acceptance criteria:** Every physical button is visible and clickable, with its key ID correctly passed to the controller.

### Step 7 — Calculator Display

**Files:**
- `src/ui/calculator_display.py`
- `test/test_display.py`

Build a two-level calculator display with an indicator region.

Display regions:

1. Status indicators
2. Current expression
3. Result area

Supported indicators in Phase 1 should include:

- SHIFT
- ALPHA
- Current mode, where applicable
- DEG / RAD / GRA
- Math display mode
- FIX / SCI, when selected

Tasks:

- [ ] Implement the display widget.
- [ ] Render the current expression.
- [ ] Render the result field, initially empty.
- [ ] Render active state indicators.
- [ ] Render input cursor position.
- [ ] Implement input overflow handling.
- [ ] Refresh display when state changes.
- [ ] Ensure the display is not directly editable through an uncontrolled text field.
- [ ] Add display rendering and indicator tests.

For Phase 1, an editable linear representation is sufficient as the underlying input buffer.

Structured fractions, roots, integral templates, natural notation, and exact mathematical formatting are implemented in Phase 2.

**Acceptance criteria:** The display always reflects current calculator state, input position, and active indicators.

### Step 8 — MODE and SETUP Menus

**Files:**
- `src/ui/menu_view.py`
- `test/test_menu.py`

Implement reusable menu presentation for calculator functions and settings.

**MODE options**

1. COMP
2. CMPLX
3. STAT
4. BASE-N
5. EQN
6. MATRIX
7. TABLE
8. VECTOR

**SETUP categories**

- Mathematical input/output display format
- Angle unit
- Number format
- Fraction result format
- Complex result format
- Statistical frequency settings
- Additional documented settings
- Display contrast behavior

Implement menu structure and navigation in this phase. Settings owned by Phase 1 must update state correctly; settings that need Phase 2 computation or rendering must be stored without pretending that their downstream effects already work.

Mode selection changes the active mode, but calculation capabilities for advanced modes remain unavailable until Phase 3.

Tasks:

- [ ] Build reusable menu widget.
- [ ] Implement numbered menu options.
- [ ] Implement multi-page menus.
- [ ] Implement numeric selection.
- [ ] Implement arrow-based navigation.
- [ ] Implement AC cancellation.
- [ ] Implement MODE selection.
- [ ] Implement SHIFT + MODE setup access.
- [ ] Implement Phase 1 setup state updates.
- [ ] Clearly distinguish selected modes from implemented calculation capabilities.
- [ ] Add menu behavior tests.

**Acceptance criteria:** Menus display correctly, accept navigation and selection, and update valid calculator settings.

### Step 9 — Keyboard and Numpad Support

**Files:**
- `src/input/keyboard.py`
- `test/test_keyboard.py`

Implement keyboard translation into the same physical actions used by mouse clicks.

Recommended initial mappings:

| Windows keyboard | Calculator input |
|---|---|
| `0–9` | Numeric keys |
| Numpad `0–9` | Numeric keys |
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `.` | Decimal point |
| `(` / `)` | Parentheses |
| `Enter` / Numpad Enter | Equals |
| `Backspace` | DEL |
| `Delete` | DEL |
| `Escape` | AC |
| Arrow keys | Calculator navigation |
| `F2` | SHIFT |
| `F3` | ALPHA |
| `F4` | MODE |
| `F5` | SETUP shortcut |

The function-key shortcuts are desktop conveniences, not claims of physical Casio keyboard equivalence. F5 must dispatch the same setup command as SHIFT + MODE.

Tasks:

- [ ] Implement keyboard-to-key/action translation.
- [ ] Implement standard number row support.
- [ ] Implement numpad support.
- [ ] Implement arithmetic operators.
- [ ] Implement Enter and editing shortcuts.
- [ ] Implement arrow navigation.
- [ ] Implement SHIFT, ALPHA, MODE, and SETUP shortcuts.
- [ ] Route input through the same controller as mouse input.
- [ ] Prevent duplicate Qt keyboard handling.
- [ ] Ensure button focus does not steal Enter or arrow keys unexpectedly.
- [ ] Ignore unsupported keyboard input safely.
- [ ] Add keyboard mapping and integration tests.

Keyboard translation must account for Qt key events, modifiers, and keypad-specific behavior rather than relying on character text alone.

**Acceptance criteria:** Keyboard and mouse interaction produce equivalent calculator state transitions.

---

## 4. Testing Strategy

Use `pytest` with PySide6's existing testing utilities where required.

Do not add unnecessary testing dependencies during Phase 1.

`test/conftest.py` should provide reusable fixtures for:

- QApplication
- Calculator state
- Calculator controller
- Main window
- Keyboard and mouse event simulation

### Required test coverage

| Test file | Coverage |
|---|---|
| `test_launch.py` | Application initialization, window visibility, shutdown |
| `test_key_registry.py` | Physical key coverage, primary/SHIFT/ALPHA mappings |
| `test_keypad.py` | Layout, key widgets, mouse dispatch |
| `test_display.py` | Expression, cursor, result region, indicators |
| `test_keyboard.py` | Keyboard, numpad, arrow keys, shortcuts |
| `test_state.py` | Defaults, state transitions, invariant checks |
| `test_controller.py` | Input, editing, modifiers, menus, power |
| `test_menu.py` | Mode selection, setup selection, navigation, cancellation |

### Critical integration scenarios

- [ ] Enter `123` using the mouse; display shows `123`.
- [ ] Enter `123` using the keyboard; state matches mouse input.
- [ ] Move cursor left and insert another digit at the correct position.
- [ ] Delete a digit using DEL and Backspace.
- [ ] Press AC and verify the expression is cleared.
- [ ] Press SHIFT and verify the indicator becomes active.
- [ ] Press a shifted-function key and verify the correct alternate action is dispatched.
- [ ] Press ALPHA and verify its alternate mapping.
- [ ] Press MODE and select COMP.
- [ ] Press MODE and select CMPLX; verify only the mode changes, not mathematical capability.
- [ ] Press SHIFT + MODE and verify SETUP opens.
- [ ] Change the angle setting and verify its indicator.
- [ ] Navigate a multi-page menu with arrow keys.
- [ ] Select a menu option using a numeric key.
- [ ] Press AC while in a menu and verify cancellation.
- [ ] Verify SHIFT + AC powers off the calculator.
- [ ] Verify ON restores interactive operation.
- [ ] Verify unimplemented calculation actions cannot produce misleading results.
- [ ] Verify no action unexpectedly crashes the application.

Tests should include direct controller tests and UI integration tests. Do not depend solely on visual screenshot comparisons.

### Test execution

Run all tests from the project root:

~~~powershell
uv run pytest test/ -v
~~~

For headless UI tests where appropriate:

~~~powershell
$env:QT_QPA_PLATFORM = "offscreen"
uv run pytest test/ -v
Remove-Item Env:QT_QPA_PLATFORM
~~~

Manual validation must still be performed in a real visible Windows desktop session.

---

## 5. Execution Order

Follow this order. Do not begin a dependent step before the relevant foundation is working.

| Order | Implementation | Required verification |
|---|---|---|
| 1 | Application entry point | Launch test |
| 2 | Action system and key registry | Registry tests |
| 3 | Calculator state | State tests |
| 4 | Controller | Controller tests |
| 5 | Main window and styles | Window rendering |
| 6 | Key widgets and keypad | Mouse dispatch tests |
| 7 | Calculator display | Display tests |
| 8 | MODE and SETUP menus | Menu tests |
| 9 | Keyboard and numpad input | Keyboard tests |
| 10 | Complete integration validation | Full test suite |

Do not expand the codebase with Phase 2 functionality merely to make Phase 1 demonstration workflows appear complete.

---

## 6. Manual Reference Verification

The official Casio user guide must be used to validate interactions before calling the foundation complete.

Reference:

https://www.casio.com/content/dam/casio/global/support/manuals/calculators/pdf/2022/mutual/fx-570ES_991ES_9910NG_PLUS_EN.pdf

Relevant sections:

- Key Markings
- Reading the Display
- Using Menus
- Calculation Modes and Calculator Setup
- Inputting Expressions and Values
- Correcting and Clearing an Expression

Before finalizing the keypad registry:

- [ ] Verify the physical key count and row/column positions against an appropriate fx-570ES PLUS-2 reference.
- [ ] Verify primary, SHIFT, and ALPHA labels.
- [ ] Verify navigation key positions.
- [ ] Verify MODE and SETUP sequences.
- [ ] Verify menu numbering and pagination.
- [ ] Verify modifier cancellation behavior.
- [ ] Verify ON/OFF and clear behavior.
- [ ] Verify which setup options belong to the target calculator rather than a related model.

Maintain the broader documented-operation feature checklist in `TASKS.md` or an appropriate later-phase plan so Phase 1 does not introduce another unnecessary registry of feature completion.

---

## 7. Phase Boundaries

### Included in Phase 1

- Native Windows application
- Full physical keypad interface
- Original visual styling
- Input and cursor state
- Action registry
- Central controller
- Display foundation
- Modifier handling
- Mode and setup menus
- Keyboard and numpad mappings
- Mouse interaction
- Initial automated testing

### Explicitly deferred

**Phase 2**
- Expression parsing
- Mathematical evaluation
- Scientific calculation implementation
- Natural Textbook Display rendering
- Advanced expression editing
- Mathematical results and formatting
- Calculation memory and replay
- Mathematical error handling

**Phase 3**
- Advanced calculation mode implementations
- Statistical, matrix, vector, and equation editors
- BASE-N evaluation
- Complex calculations
- TABLE calculations

**Phase 4**
- Full compatibility validation
- Numerical precision and behavior testing
- Boundary and performance testing

**Phase 5**
- Persistent preferences
- User-configurable shortcuts
- Windows executable packaging
- Installer and release validation

The UI and controller must allow these capabilities to be introduced without requiring a major redesign.

---

## 8. Quality Requirements

### Code quality

- Use Python 3.10-compatible syntax.
- Use clear type annotations.
- Keep each module focused on one responsibility.
- Avoid unnecessary abstract base classes and generic frameworks.
- Avoid global mutable calculator state.
- Keep key definitions centralized.
- Keep Qt-specific code outside pure state and action models.
- Prefer simple functions and small classes.
- Avoid hardcoded calculator behavior inside individual button widgets.

### Interface quality

- All keys are visible and usable.
- Labels are readable at supported window sizes.
- Modifier indicators are unambiguous.
- Menu navigation has visible feedback.
- Mouse and keyboard workflows are consistent.
- No input is silently lost because of focus issues.
- No incomplete mathematical operation displays a fabricated answer.

### Testing quality

- All completed foundation behaviors have automated tests.
- Modifier transitions cover normal and edge cases.
- Menu operations cover valid, invalid, and cancellation paths.
- Keyboard tests include number-row and numpad input.
- Tests are deterministic.
- No tests require an internet connection.
- No failing tests are ignored to declare the phase complete.

---

## 9. Final Validation Checklist

### Application

- [ ] Application launches from the configured project environment.
- [ ] Main window appears correctly.
- [ ] Application exits cleanly.

### UI

- [ ] Physical keypad is complete.
- [ ] All primary and alternate labels are represented.
- [ ] Calculator display renders correctly.
- [ ] Styling is consistent.
- [ ] Layout remains usable at supported window dimensions.

### Input

- [ ] All physical keys dispatch valid actions.
- [ ] Mouse clicks work.
- [ ] Keyboard input works.
- [ ] Numpad input works.
- [ ] Arrow navigation works.
- [ ] Editing works.

### State and control

- [ ] SHIFT works.
- [ ] ALPHA works.
- [ ] DEL works.
- [ ] AC works.
- [ ] MODE works.
- [ ] SETUP works.
- [ ] ON/OFF state handling works.
- [ ] Menu cancellation works.
- [ ] Mode transitions update state.
- [ ] Setup changes update state.

### Architecture

- [ ] No duplicated action routing.
- [ ] No mathematical calculations embedded in UI components.
- [ ] No controller logic in keyboard mapping.
- [ ] No unexpected circular dependencies.
- [ ] Phase 2 extension points are clear.

### Tests

- [ ] Launch tests pass.
- [ ] Registry tests pass.
- [ ] State tests pass.
- [ ] Controller tests pass.
- [ ] Keypad tests pass.
- [ ] Display tests pass.
- [ ] Keyboard tests pass.
- [ ] Menu tests pass.
- [ ] Manual Windows interaction tests pass.

---

## 10. Definition of Done

Phase 1 is complete only when:

1. The application launches reliably on the target Windows environment.
2. The full calculator keypad is rendered with its correct physical action mappings.
3. All foundation actions work with mouse and keyboard input.
4. SHIFT, ALPHA, DEL, AC, MODE, SETUP, cursor navigation, and menu selection behave correctly.
5. The display accurately reflects the current calculator state.
6. Every physical key dispatches its registered action, including actions reserved for subsequent phases.
7. All automated foundation tests pass.
8. Manual interaction validation succeeds.
9. No known critical foundation defects remain.
10. Completed tasks in `TASKS.md` are updated only after implementation and verification.

**Phase 1 deliverable:** A functional, interactive Windows scientific calculator shell with a complete control system, ready for mathematical engine integration in Phase 2.
