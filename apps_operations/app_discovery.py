from pathlib import Path
import json
import win32com.client
import winreg
import subprocess


from apps_operations.app_registry import create_aliases


APPS_FILE = Path("config/apps.json")


# ============================================================
# START MENU DISCOVERY
# ============================================================

def discover_start_menu_apps():
    start_menu_locations = [
        (
            Path.home()
            / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
        ),
        (
            Path("C:/ProgramData")
            / "Microsoft/Windows/Start Menu/Programs"
        )
    ]

    shell = win32com.client.Dispatch("WScript.Shell")

    apps = []

    for start_menu in start_menu_locations:

        if not start_menu.exists():
            continue

        for shortcut in start_menu.rglob("*.lnk"):

            try:
                link = shell.CreateShortCut(str(shortcut))

                target_path = link.Targetpath

                if not target_path:
                    continue

                target = Path(target_path)

                if not target.exists():
                    continue

                if not target.is_file():
                    continue

                if target.suffix.lower() != ".exe":
                    continue

                app = {
                    "name": shortcut.stem,
                    "target": str(target),
                    "arguments": link.Arguments or "",
                    "working_directory": (
                        link.WorkingDirectory
                        if link.WorkingDirectory
                        else str(target.parent)
                    ),
                    "shortcut": str(shortcut),
                    "source": "start_menu"
                }

                apps.append(app)

            except Exception:
                continue

    return apps


# ============================================================
# REGISTRY DISCOVERY
# ============================================================

def discover_registry_apps():

    registry_locations = [
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        ),
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ),
        (
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        )
    ]

    apps = []

    for hive, registry_path in registry_locations:

        try:
            root_key = winreg.OpenKey(hive, registry_path)

        except OSError:
            continue

        try:
            subkey_count = winreg.QueryInfoKey(root_key)[0]

            for index in range(subkey_count):

                try:
                    subkey_name = winreg.EnumKey(root_key, index)

                    subkey = winreg.OpenKey(
                        root_key,
                        subkey_name
                    )

                except OSError:
                    continue

                try:
                    try:
                        name = winreg.QueryValueEx(
                            subkey,
                            "DisplayName"
                        )[0]

                    except OSError:
                        continue

                    if not name:
                        continue

                    try:
                        install_location = winreg.QueryValueEx(
                            subkey,
                            "InstallLocation"
                        )[0]

                    except OSError:
                        install_location = ""

                    try:
                        display_icon = winreg.QueryValueEx(
                            subkey,
                            "DisplayIcon"
                        )[0]

                    except OSError:
                        display_icon = ""

                    target = find_executable(
                        install_location,
                        display_icon
                    )

                    app = {
                        "name": name,
                        "target": str(target) if target else "",
                        "arguments": "",
                        "working_directory": (
                            str(target.parent)
                            if target
                            else install_location
                        ),
                        "shortcut": "",
                        "source": "registry"
                    }

                    apps.append(app)

                finally:
                    winreg.CloseKey(subkey)

        finally:
            winreg.CloseKey(root_key)

    return apps


# ============================================================
# FIND EXECUTABLE
# ============================================================

def find_executable(install_location, display_icon):

    # --------------------------------------------------------
    # Try DisplayIcon first
    # --------------------------------------------------------

    if display_icon:

        icon_path = str(display_icon)

        # Remove icon index such as:
        # application.exe,0
        if "," in icon_path:
            icon_path = icon_path.split(",", 1)[0]

        icon_path = icon_path.strip('"')

        path = Path(icon_path)

        if path.exists() and path.is_file():
            if path.suffix.lower() == ".exe":
                return path

    # --------------------------------------------------------
    # Try InstallLocation
    # --------------------------------------------------------

    if install_location:

        install_path = Path(install_location)

        if install_path.exists() and install_path.is_dir():

            # Look for executables directly inside directory
            executables = list(
                install_path.glob("*.exe")
            )

            if executables:
                return executables[0]

            # Search one level deeper
            executables = list(
                install_path.glob("*/*.exe")
            )

            if executables:
                return executables[0]

    return None


# ============================================================
# MICROSOFT STORE / APPX DISCOVERY
# ============================================================

def discover_store_apps():

    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        (
            "Get-AppxPackage | "
            "Select-Object Name, InstallLocation | "
            "ConvertTo-Json -Compress"
        )
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    except Exception:
        return []

    if result.returncode != 0:
        return []

    if not result.stdout.strip():
        return []

    try:
        data = json.loads(result.stdout)

    except json.JSONDecodeError:
        return []

    # PowerShell returns an object instead of an array
    # when there is only one result.
    if isinstance(data, dict):
        data = [data]

    apps = []

    for package in data:

        name = package.get("Name")
        install_location = package.get("InstallLocation")

        if not name:
            continue

        if not install_location:
            continue

        location = Path(install_location)

        if not location.exists():
            continue

        app = {
            "name": name,
            "target": "",
            "arguments": "",
            "working_directory": str(location),
            "shortcut": "",
            "source": "store"
        }

        apps.append(app)

    return apps


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(apps):

    unique_apps = {}

    for app in apps:

        target = app.get("target", "").lower().strip()

        name = app.get("name", "").lower().strip()

        # Prefer executable path as unique identifier
        if target:
            key = f"target:{target}"

        else:
            key = f"name:{name}"

        if key not in unique_apps:

            unique_apps[key] = app

        else:

            existing = unique_apps[key]

            # Prefer Start Menu entry because it usually
            # contains the actual executable and arguments.
            if (
                existing.get("source") != "start_menu"
                and app.get("source") == "start_menu"
            ):
                unique_apps[key] = app

    return list(unique_apps.values())


# ============================================================
# CLEAN APPLICATION DATA
# ============================================================

def clean_apps(apps):

    cleaned = []

    for app in apps:

        # Skip completely unusable applications
        if not app.get("name"):
            continue

        # Store apps may not have a direct executable.
        # Keep them because they can be handled later.
        if (
            app.get("source") != "store"
            and not app.get("target")
        ):
            continue

        cleaned.append(app)

    return cleaned


# ============================================================
# ALIASES
# ============================================================

def add_aliases(apps):

    for app in apps:

        app["aliases"] = create_aliases(
            app["name"]
        )

    return apps


# ============================================================
# SAVE
# ============================================================

def save_apps(apps):

    APPS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        APPS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            apps,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# MAIN DISCOVERY
# ============================================================

def discover_apps():

    apps = []

    start_menu_apps = discover_start_menu_apps()

    apps.extend(start_menu_apps)

    registry_apps = discover_registry_apps()

    apps.extend(registry_apps)

    store_apps = discover_store_apps()

    apps.extend(store_apps)

    # --------------------------------------------------------
    # Clean
    # --------------------------------------------------------

    apps = clean_apps(apps)

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    apps = remove_duplicates(apps)

    # --------------------------------------------------------
    # Add aliases
    # --------------------------------------------------------

    apps = add_aliases(apps)

    # --------------------------------------------------------
    # Sort alphabetically
    # --------------------------------------------------------

    apps.sort(
        key=lambda app: app["name"].lower()
    )

    return apps


# ============================================================
# DISCOVER + SAVE
# ============================================================

def discover_and_save_apps():

    apps = discover_apps()

    save_apps(apps)

    return apps