# PHASE-5.md — Windows Release

**Project:** Scientific Calculator — fx-570ES PLUS-2 Inspired  
**Phase:** 5 — Windows Release  
**Status:** Completed  
**Target:** Windows 10/11 (Standalone Offline Desktop)  
**Python:** 3.10.11  
**Dependencies:** PySide6, SymPy, pytest, uv, PyInstaller  

---

## 1. Objective

Deliver a standalone, production-ready Windows desktop release of the scientific calculator that runs completely offline without requiring Python or external runtimes on user systems.

### Key Release Requirements:
1. **Persistent Preferences & Settings:**
   - Save and restore angle unit (`DEG`/`RAD`/`GRA`), display format (`MthIO`/`LineIO`), number format (`Norm`/`Fix`/`Sci`), fraction mode (`d/c`/`ab/c`), complex format (`a+bi`/`r∠θ`), and stat frequency across sessions.
   - Save and restore window geometry and layout dimensions.
   - Support configurable keyboard shortcut mapping.
2. **Branding, Iconography & Metadata:**
   - Create multi-resolution `.ico` and `.png` application icons featuring the authentic Casio 2nd Edition design.
   - Define canonical version metadata (`version = "2.0.0"`, author, copyright, description).
   - Apply native application icon to the window shell and taskbar.
3. **Standalone Executable Packaging:**
   - Build a standalone Windows executable using PyInstaller with `--windowed --noconsole`.
   - Embed Windows version info resources (FileDescription, ProductVersion, LegalCopyright).
   - Ensure all PySide6 and SymPy plugins, math modules, and icons are packaged cleanly.
4. **Verification & Quality Checks:**
   - Automated test suite covering settings serialization, icon validity, version info, and entry point.
   - Run full regression suite across all phases.
5. **Release Documentation:**
   - User installation and quickstart guide with physical keyboard shortcut reference.
   - Update `TASKS.md` marking all milestones and completion criteria done.

---

## 2. Architecture & File Layout

```text
fx-570ES-PLUS-2/
│
├── src/
│   ├── version.py              # Application version, metadata, and branding constants
│   ├── core/
│   │   ├── preferences.py      # Persistent settings manager (QSettings / JSON storage)
│   │   └── ...
│   ├── ui/
│   │   ├── assets/
│   │   │   ├── icon.ico        # Multi-resolution Windows application icon
│   │   │   └── icon.png        # High-res 256x256 application icon
│   │   ├── main_window.py      # Integrated with preferences, icon, and window geometry
│   │   └── ...
│   └── input/
│       └── keyboard.py         # Configurable shortcut dictionary
│
├── scripts/
│   ├── generate_icon.py        # Generates icon.ico and icon.png programmatically
│   └── build_windows.py        # PyInstaller automated packaging script
│
├── test/
│   └── test_phase5_release.py  # Tests for preferences, icon, version, shortcuts
│
└── TASKS.md                    # Project tracking
```

---

## 3. Step-by-Step Execution Plan

- [x] **Step 1:** Implement `src/version.py` with version info, metadata, and application constants.
- [x] **Step 2:** Implement `src/core/preferences.py` with persistent storage (save/load setup options, window geometry).
- [x] **Step 3:** Implement `scripts/generate_icon.py` and produce `src/ui/assets/icon.png` and `src/ui/assets/icon.ico`.
- [x] **Step 4:** Integrate application icon and preferences into `src/ui/main_window.py` and `src/main.py`.
- [x] **Step 5:** Add configurable shortcut capabilities in `src/input/keyboard.py`.
- [x] **Step 6:** Implement `test/test_phase5_release.py` and verify all tests pass.
- [x] **Step 7:** Build standalone executable using PyInstaller via `scripts/build_windows.py`.
- [x] **Step 8:** Verify standalone executable launches and runs cleanly.
- [x] **Step 9:** Update `README.md` and `TASKS.md` marking all Phase 5 tasks and criteria complete.
- [x] **Step 10:** Git Commit, Push, Open PR via `gh`, Merge to `main`, and Report.
