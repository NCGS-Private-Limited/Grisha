import re


# ============================================================
# ERROR KEYWORDS
# ============================================================

ERROR_KEYWORDS = [
    "error",
    "exception",
    "traceback",
    "failed",
    "failure",
    "fatal",
    "critical",
    "not found",
    "invalid",
    "cannot",
    "could not"
]


# ============================================================
# APPLICATION TYPE DETECTION
# ============================================================

def detect_application_type(
    application,
    window_title,
    visible_text
):

    text = (
        f"{application or ''} "
        f"{window_title or ''} "
        f"{visible_text or ''}"
    ).lower()

    # --------------------------------------------------------
    # Code editor
    # --------------------------------------------------------

    if (
        "visual studio code" in text
        or "vs code" in text
        or "code.exe" in text
    ):
        return "code_editor"

    # --------------------------------------------------------
    # Terminal
    # --------------------------------------------------------

    if (
        "powershell" in text
        or "command prompt" in text
        or "cmd.exe" in text
        or "terminal" in text
    ):
        return "terminal"

    # --------------------------------------------------------
    # Browser
    # --------------------------------------------------------

    browser_names = [
        "google chrome",
        "microsoft edge",
        "mozilla firefox"
    ]

    for browser in browser_names:

        if browser in text:
            return "browser"

    return "unknown"


# ============================================================
# DETECT ACTIVE FILE
# ============================================================

def detect_active_file(
    window_title,
    visible_text
):

    # --------------------------------------------------------
    # Common filename extensions
    # --------------------------------------------------------

    extensions = (
        "py",
        "js",
        "ts",
        "tsx",
        "jsx",
        "cpp",
        "c",
        "h",
        "hpp",
        "java",
        "cs",
        "go",
        "rs",
        "html",
        "css",
        "json",
        "xml",
        "yaml",
        "yml",
        "md",
        "txt"
    )

    # --------------------------------------------------------
    # Search window title
    # --------------------------------------------------------

    if window_title:

        pattern = (
            r"\b[\w .()-]+\."
            r"(?:" + "|".join(extensions) + r")\b"
        )

        matches = re.findall(
            pattern,
            window_title,
            re.IGNORECASE
        )

        if matches:

            # The last matching filename is usually
            # the actual file name.
            return matches[-1].strip()

    # --------------------------------------------------------
    # Search visible text
    # --------------------------------------------------------

    if visible_text:

        pattern = (
            r"\b[\w.-]+\."
            r"(?:" + "|".join(extensions) + r")\b"
        )

        matches = re.findall(
            pattern,
            visible_text,
            re.IGNORECASE
        )

        if matches:
            return matches[0].strip()

    return None


# ============================================================
# DETECT CODE
# ============================================================

def detect_code(
    visible_text
):

    if not visible_text:
        return False

    code_patterns = [
        r"\bdef\s+\w+\s*\(",
        r"\bclass\s+\w+",
        r"\bimport\s+\w+",
        r"\bfrom\s+\w+\s+import\b",
        r"\bif\s+.+:",
        r"\bfor\s+\w+\s+in\b",
        r"\bwhile\s+.+:",
        r"\bprint\s*\(",
        r"\breturn\s+",
        r"[{};]\s*$"
    ]

    for pattern in code_patterns:

        if re.search(
            pattern,
            visible_text,
            re.MULTILINE
        ):
            return True

    return False


# ============================================================
# DETECT TERMINAL
# ============================================================

def detect_terminal(elements, visible_text):

    text = (
        visible_text or ""
    ).lower()

    # --------------------------------------------------------
    # UI element detection
    # --------------------------------------------------------

    for element in elements:

        element_text = (
            element.get("text", "")
            .lower()
        )

        if "terminal" in element_text:
            return True

    # --------------------------------------------------------
    # Text detection
    # --------------------------------------------------------

    terminal_patterns = [
        r"PS\s+[A-Za-z]:\\",
        r"[A-Za-z]:\\.*>",
        r"Microsoft Windows",
        r"Command Prompt",
        r"PowerShell"
    ]

    for pattern in terminal_patterns:

        if re.search(
            pattern,
            visible_text or "",
            re.IGNORECASE
        ):
            return True

    return False

def looks_like_source_code(line):

    source_patterns = [
        r"^\s*(return|print|import|from|def|class|if|elif|else|for|while|try|except|finally|with)\b",
        r"^\s*[\w.]+\s*=\s*",
        r"\breturn\s+['\"]",
        r"\bprint\s*\(",
        r"\bdef\s+\w+\s*\(",
        r"\bclass\s+\w+",
        r"['\"].*(error|failed|failure|not found|invalid).*['\"]",
        r"\b(error|failed|failure|invalid)\b.*:"
    ]

    for pattern in source_patterns:

        if re.search(
            pattern,
            line,
            re.IGNORECASE
        ):
            return True

    return False


# ============================================================
# DETECT ERRORS
# ============================================================

def detect_errors(visible_text):

    if not visible_text:
        return []

    errors = []

    lines = visible_text.splitlines()

    # --------------------------------------------------------
    # Strong error indicators
    # --------------------------------------------------------

    strong_patterns = [
        r"Traceback \(most recent call last\)",
        r"\b[A-Za-z]+Error:",
        r"\b[A-Za-z]+Exception:",
        r"\bModuleNotFoundError:",
        r"\bNameError:",
        r"\bSyntaxError:",
        r"\bTypeError:",
        r"\bValueError:",
        r"\bAttributeError:",
        r"\bImportError:",
        r"\bFileNotFoundError:",
        r"\bPermissionError:",
        r"\bConnectionError:",
        r"\bFatal error\b",
        r"\bUnhandled exception\b"
    ]

    # --------------------------------------------------------
    # Check lines
    # --------------------------------------------------------

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        # ----------------------------------------------------
        # Ignore source-code lines
        # ----------------------------------------------------

        if looks_like_source_code(
            stripped
        ):
            continue

        # ----------------------------------------------------
        # Strong error patterns
        # ----------------------------------------------------

        for pattern in strong_patterns:

            if re.search(
                pattern,
                stripped,
                re.IGNORECASE
            ):

                errors.append({
                    "text": stripped,
                    "type": "error",
                    "confidence": "high"
                })

                break

    return errors


# ============================================================
# DESCRIBE SCREEN
# ============================================================

def understand_screen(
    context,
    all_windows=None
):

    if not context:
        return {
            "understood": False,
            "description": (
                "Unable to determine "
                "screen context."
            )
        }

    # Existing foreground analysis
    application = context.get(
        "application"
    )

    process = context.get(
        "process"
    )

    window = context.get(
        "window"
    )

    visible_text = context.get(
        "visible_text",
        ""
    )

    elements = context.get(
        "elements",
        []
    )

    # --------------------------------------------------------
    # Existing analysis
    # --------------------------------------------------------

    application_name = None

    if application:
        application_name = application.get(
            "name"
        )

    window_title = ""

    if window:
        window_title = window.get(
            "title",
            ""
        )

    application_type = detect_application_type(
        application_name,
        window_title,
        visible_text
    )

    active_file = detect_active_file(
        window_title,
        visible_text
    )

    contains_code = detect_code(
        visible_text
    )

    terminal_visible = detect_terminal(
        elements,
        visible_text
    )

    errors = detect_errors(
        visible_text
    )

    # --------------------------------------------------------
    # Build complete understanding
    # --------------------------------------------------------

    understanding = {
        "understood": True,

        "foreground": {
            "application": application_name,
            "window": window_title,
            "hwnd": (
                window.get("hwnd")
                if window
                else None
            ),
            "pid": (
                window.get("pid")
                if window
                else None
            )
        },

        "windows": all_windows or [],

        "active_file": active_file,

        "contains_code": contains_code,

        "terminal_visible": terminal_visible,

        "errors": errors,

        "visible_text": visible_text,

        "elements": elements
    }

    return understanding


# ============================================================
# GENERATE HUMAN DESCRIPTION
# ============================================================

def describe_screen(understanding):

    if not understanding.get("understood"):

        return understanding.get(
            "description",
            "Unable to understand screen."
        )

    lines = []

    # ========================================================
    # VISIBLE WINDOWS
    # ========================================================

    windows = understanding.get(
        "windows",
        []
    )

    if windows:

        lines.append(
            f"I can see {len(windows)} "
            f"visible window"
            f"{'s' if len(windows) != 1 else ''}."
        )

        lines.append("")

        for item in windows:

            application = item.get(
                "application"
            )

            window = item.get(
                "window",
                {}
            )

            app_name = "Unknown"

            if application:

                app_name = application.get(
                    "name",
                    "Unknown"
                )

            title = window.get(
                "title",
                ""
            )

            if item.get("foreground"):

                lines.append(
                    f"[FOREGROUND] "
                    f"{app_name}"
                )

            else:

                lines.append(
                    f"{app_name}"
                )

            if title:

                lines.append(
                    f"  Window: {title}"
                )

    # ========================================================
    # FOREGROUND DETAILS
    # ========================================================

    foreground = understanding.get(
        "foreground",
        {}
    )

    foreground_application = (
        foreground.get("application")
    )

    if foreground_application:

        lines.append("")

        lines.append(
            f"Currently focused: "
            f"{foreground_application}."
        )

    # ========================================================
    # ACTIVE FILE
    # ========================================================

    active_file = understanding.get(
        "active_file"
    )

    if active_file:

        lines.append(
            f"The active file appears "
            f"to be {active_file}."
        )

    # ========================================================
    # CODE
    # ========================================================

    if understanding.get(
        "contains_code"
    ):

        lines.append(
            "The screen appears to "
            "contain source code."
        )

    # ========================================================
    # TERMINAL
    # ========================================================

    if understanding.get(
        "terminal_visible"
    ):

        lines.append(
            "A terminal panel appears "
            "to be visible."
        )

    # ========================================================
    # ERRORS
    # ========================================================

    errors = understanding.get(
        "errors",
        []
    )

    if errors:

        lines.append(
            f"I detected {len(errors)} "
            f"likely error message"
            f"{'s' if len(errors) != 1 else ''}."
        )

    # ========================================================
    # FALLBACK
    # ========================================================

    if not lines:

        return (
            "I can see the screen, but "
            "I could not determine its "
            "contents reliably."
        )

    return "\n".join(lines)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from screen_operations.screen_capture import (
        capture_screen
    )

    from screen_operations.screen_processor import (
        process_screen
    )

    from screen_operations.application_context import (
        get_application_context
    )

    print("Capturing screen...")

    screenshot = capture_screen()

    if screenshot is None:

        print("Failed to capture screen.")

    else:

        screenshot = process_screen(
            screenshot
        )

        print(
            "Building application context..."
        )

        context = get_application_context(
            screenshot
        )

        print(
            "Understanding screen..."
        )

        understanding = understand_screen(
            context
        )

        print()
        print("=" * 60)
        print("SCREEN UNDERSTANDING")
        print("=" * 60)
        print()

        print(
            describe_screen(
                understanding
            )
        )

        print()
        print("Detected errors:")

        for error in understanding[
            "errors"
        ]:

            print(
                f"  {error['text']}"
            )