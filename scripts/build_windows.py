"""Automated PyInstaller build script for Casio fx-570ES PLUS 2 Windows standalone release."""
import os
import subprocess
import sys
import shutil


def build():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    app_entry = os.path.join(root_dir, "src", "app.py")
    icon_path = os.path.join(root_dir, "src", "ui", "assets", "icon.ico")
    assets_dir = os.path.join(root_dir, "src", "ui", "assets")
    dist_dir = os.path.join(root_dir, "dist")
    build_dir = os.path.join(root_dir, "build")

    print("==================================================")
    print("Building Casio fx-570ES PLUS 2nd Edition Windows Release")
    print("==================================================")

    # 1. Ensure icons exist
    if not os.path.exists(icon_path):
        print("Generating icons first...")
        from scripts.generate_icon import main as gen_icons
        gen_icons()

    # 2. Clean previous dist/build if present
    target_dist = os.path.join(dist_dir, "Casio-fx570ES-PLUS-2")
    if os.path.exists(target_dist):
        try:
            shutil.rmtree(target_dist)
        except Exception:
            pass

    # 3. PyInstaller command arguments
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconsole",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--name", "Casio-fx570ES-PLUS-2",
        "--icon", icon_path,
        "--add-data", f"{assets_dir};src/ui/assets",
        "--collect-submodules", "sympy",
        "--collect-submodules", "mpmath",
        app_entry,
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=root_dir)

    if result.returncode != 0:
        print("Error: PyInstaller build failed!")
        sys.exit(result.returncode)

    exe_path = os.path.join(dist_dir, "Casio-fx570ES-PLUS-2", "Casio-fx570ES-PLUS-2.exe")
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print("\n==================================================")
        print(f"Build SUCCESSFUL!")
        print(f"Standalone executable located at: {exe_path}")
        print(f"Executable size: {size_mb:.2f} MB")
        print("==================================================")
    else:
        print(f"Warning: Executable not found at {exe_path}")


if __name__ == "__main__":
    build()
