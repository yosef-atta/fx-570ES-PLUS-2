"""Automated Windows installer for Casio fx-570ES PLUS 2nd Edition.
Installs the standalone application into %LocalAppData%\\Programs\\Casio-fx570ES-PLUS-2,
registers Start Menu and Desktop shortcuts, and registers in Windows Installed Apps.
"""
import os
import shutil
import subprocess
import sys
import winreg

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.version import (
    APP_NAME,
    APP_SHORT_NAME,
    VERSION,
    AUTHOR,
    DESCRIPTION,
)


def create_windows_shortcut(target_exe: str, shortcut_path: str, working_dir: str, icon_path: str, description: str):
    """Creates a Windows .lnk shortcut using PowerShell WScript.Shell COM object."""
    ps_command = f"""
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
    $Shortcut.TargetPath = "{target_exe}"
    $Shortcut.WorkingDirectory = "{working_dir}"
    $Shortcut.IconLocation = "{icon_path},0"
    $Shortcut.Description = "{description}"
    $Shortcut.Save()
    """
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_command], check=True)


def register_in_windows_apps(install_dir: str, exe_path: str, icon_path: str):
    """Registers the application in Windows 'Installed Apps' / Settings > Apps."""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Casio-fx570ES-PLUS-2"
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, APP_NAME)
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, VERSION)
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, AUTHOR)
            winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, icon_path)
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, install_dir)
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'powershell -NoProfile -Command "Remove-Item -Recurse -Force \'{install_dir}\'"')
            winreg.SetValueEx(key, "NoModify", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "NoRepair", 0, winreg.REG_DWORD, 1)
    except Exception as e:
        print(f"Warning: Could not register in Windows Uninstall list: {e}")


def get_real_desktop_dir() -> str:
    """Returns the actual Desktop path even if redirected (e.g. OneDrive)."""
    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "[Environment]::GetFolderPath('Desktop')"],
            capture_output=True,
            text=True,
            check=True,
        )
        p = res.stdout.strip()
        if p and os.path.exists(p):
            return p
    except Exception:
        pass
    return os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Desktop")


def install():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dist_dir = os.path.join(root_dir, "dist", "Casio-fx570ES-PLUS-2")
    src_exe = os.path.join(dist_dir, "Casio-fx570ES-PLUS-2.exe")
    src_icon = os.path.join(root_dir, "src", "ui", "assets", "icon.ico")

    if not os.path.exists(src_exe):
        print("Dist executable not found. Running build first...")
        from scripts.build_windows import build
        build()

    # 1. Target directory: %LocalAppData%\Programs\Casio-fx570ES-PLUS-2
    local_appdata = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
    install_dir = os.path.join(local_appdata, "Programs", "Casio-fx570ES-PLUS-2")
    os.makedirs(install_dir, exist_ok=True)

    print(f"Installing to: {install_dir} ...")

    # 2. Copy all files from dist to install directory
    for item in os.listdir(dist_dir):
        s = os.path.join(dist_dir, item)
        d = os.path.join(install_dir, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d, ignore_errors=True)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    # Copy icon to installation root for permanent shortcut reference
    dest_icon = os.path.join(install_dir, "app.ico")
    shutil.copy2(src_icon, dest_icon)

    target_exe = os.path.join(install_dir, "Casio-fx570ES-PLUS-2.exe")

    # 3. Create Start Menu Shortcuts
    appdata = os.environ.get("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
    start_menu_dir = os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs")
    os.makedirs(start_menu_dir, exist_ok=True)

    shortcuts = [
        f"{APP_NAME}.lnk",
        "fx-570ES PLUS 2nd Edition.lnk",
    ]
    for sc_name in shortcuts:
        start_shortcut = os.path.join(start_menu_dir, sc_name)
        create_windows_shortcut(
            target_exe=target_exe,
            shortcut_path=start_shortcut,
            working_dir=install_dir,
            icon_path=dest_icon,
            description=f"{APP_NAME} Scientific Calculator fx",
        )

    # 4. Create Desktop Shortcut
    desktop_dir = get_real_desktop_dir()
    if os.path.exists(desktop_dir):
        desktop_shortcut = os.path.join(desktop_dir, f"{APP_NAME}.lnk")
        create_windows_shortcut(
            target_exe=target_exe,
            shortcut_path=desktop_shortcut,
            working_dir=install_dir,
            icon_path=dest_icon,
            description=f"{APP_NAME} Scientific Calculator fx",
        )

    # 5. Register in Windows Settings / Apps
    register_in_windows_apps(install_dir, target_exe, dest_icon)

    print("\n=======================================================")
    print("SUCCESS: Casio fx-570ES PLUS 2nd Edition Installed!")
    print(f"Location: {install_dir}")
    print("Now you can open Start Menu, type 'fx' or 'Casio', and launch it directly!")
    print("=======================================================")


if __name__ == "__main__":
    install()
