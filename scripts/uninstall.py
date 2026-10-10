"""Uninstaller for Casio fx-570ES PLUS 2nd Edition."""
import os
import shutil
import sys
import winreg

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.version import APP_NAME


def uninstall():
    local_appdata = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
    install_dir = os.path.join(local_appdata, "Programs", "Casio-fx570ES-PLUS-2")

    appdata = os.environ.get("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
    start_shortcut = os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs", f"{APP_NAME}.lnk")

    desktop_dir = os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Desktop")
    desktop_shortcut = os.path.join(desktop_dir, f"{APP_NAME}.lnk")

    # 1. Remove Start Menu shortcut
    if os.path.exists(start_shortcut):
        try:
            os.remove(start_shortcut)
            print(f"Removed: {start_shortcut}")
        except Exception as e:
            print(f"Could not remove Start Menu shortcut: {e}")

    # 2. Remove Desktop shortcut
    if os.path.exists(desktop_shortcut):
        try:
            os.remove(desktop_shortcut)
            print(f"Removed: {desktop_shortcut}")
        except Exception as e:
            print(f"Could not remove Desktop shortcut: {e}")

    # 3. Remove Registry entry
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Casio-fx570ES-PLUS-2")
        print("Removed from Windows Apps registry.")
    except Exception:
        pass

    # 4. Remove installation folder
    if os.path.exists(install_dir):
        try:
            shutil.rmtree(install_dir, ignore_errors=True)
            print(f"Removed: {install_dir}")
        except Exception as e:
            print(f"Could not remove install directory: {e}")

    print("Uninstallation completed successfully.")


if __name__ == "__main__":
    uninstall()
