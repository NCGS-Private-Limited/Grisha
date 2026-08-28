# Grisha

**Grisha** is a Python-based desktop AI assistant being developed as a long-term project for natural-language computer interaction.

The goal is to build an assistant that can understand what is happening on a computer screen and perform useful actions through applications, files, folders, system controls, mouse, and keyboard.

> **Current milestone: V1 — F1.18 completed**

---

## Current Capabilities

Grisha V1 has progressed from a terminal-based command assistant into a system capable of interacting with the Windows desktop.

### Core Assistant

- Terminal-based interaction
- Command parsing and dispatching
- Configurable assistant settings
- Logging
- Error/status handling

### Memory

- Instant memory
- Permanent memory foundation
- `remember`-style functionality

### Files & Folders

- File operations
- Folder operations
- Basic filesystem interaction

### Applications

- Discover installed/start-menu applications
- Build an application database
- Open applications
- Close applications
- Focus application windows

### System Control

Grisha can perform system-level commands such as:

- Lock
- Sleep
- Restart
- Shutdown
- Hibernate

### Screen Observation

Grisha can capture and inspect the desktop using:

- Screenshot capture
- OCR
- Multiple OCR preprocessing methods
- OCR confidence filtering
- Duplicate detection/removal
- Screen element coordinates

### Mouse Control

Grisha can:

- Get mouse position
- Move the mouse
- Move relative to the current position
- Left click
- Right click
- Double click
- Control mouse button down/up
- Validate mouse coordinates

### Keyboard Control

Grisha can:

- Type text
- Press keys
- Use special keys
- Use modifier keys
- Execute keyboard shortcuts

### Screen-Based Interaction

Grisha can combine screenshot observation and OCR to interact with visible elements.

For example:

```text
click Save
```

can become:

```text
Screenshot
    ↓
OCR
    ↓
Find "Save"
    ↓
Get element coordinates
    ↓
Move mouse
    ↓
Click
```

Similarly:

```text
type Username hello world
```

can become:

```text
Screenshot
    ↓
OCR
    ↓
Find "Username"
    ↓
Click field
    ↓
Type text
```

### Multiple Element Selection

When multiple matching elements are detected, Grisha does not blindly select the first result.

Example:

```text
Multiple "Reload" elements found:

1. Reload — (1331, 279)
2. Reload — (1461, 258)

Which one do you want to use?
> 2
```

The selection system supports:

- Multiple-match detection
- Numbered choices
- Invalid-input validation
- Cancellation
- Reusable selection for mouse and keyboard actions

OCR duplicates are also deduplicated so the same physical element is not repeatedly presented as different choices.

---

# F1 Roadmap

The first development phase has focused on building the foundations required for desktop interaction.

| Version | Feature | Status |
|---|---|---|
| F1.1 | Core assistant foundation | ✅ |
| F1.2 | Command/parser system | ✅ |
| F1.3 | Dispatcher | ✅ |
| F1.4 | Configuration | ✅ |
| F1.5 | Logging | ✅ |
| F1.6 | File/folder operations | ✅ |
| F1.7 | Memory foundation | ✅ |
| F1.13 | Open applications | ✅ |
| F1.14 | Close applications | ✅ |
| F1.15 | Window focus | ✅ |
| F1.16 | System commands | ✅ |
| F1.17 | Screen observation | ✅ |
| F1.18 | Mouse, keyboard & screen interaction | ✅ |

> Some intermediate F1 versions are omitted from this overview for brevity. The repository history contains the development progression.

---

# F1.18 Architecture

The current interaction pipeline is based on four major stages:

```text
User Command
     ↓
Command Parser
     ↓
Dispatcher
     ↓
Action
     ↓
Screenshot + OCR
     ↓
Element Resolution
     ↓
Mouse / Keyboard
```

For screen-based actions:

```text
Screenshot
    ↓
Preprocessing
    ↓
OCR
    ↓
Element Detection
    ↓
Deduplication
    ↓
Element Selection
    ↓
Action
```

This architecture provides the foundation for future GUI understanding.

---

# Technologies

Grisha V1 currently uses Python and several libraries for Windows desktop interaction and screen processing.

Main technologies include:

- **Python**
- **PyAutoGUI** — mouse, keyboard, and screenshot interaction
- **Tesseract OCR**
- **pytesseract** — Python interface for Tesseract
- **Pillow** — image processing
- **pywin32** — Windows application/window interaction

---

# Project Structure

The exact structure may evolve as Grisha is refactored, but the project is organized around:

```text
F1/
├── actions/
├── apps_operations/
├── file_operations/
├── folder_operations/
├── system_operations/
├── screen_operations/
├── core/
├── config/
├── test/
└── main.py
```

---

# Example Commands

Examples of the types of commands supported during V1 development:

```text
open vscode
```

```text
close vscode
```

```text
focus vscode
```

```text
lock
```

```text
click Save
```

```text
type Username hello world
```

```text
remember ...
```

The exact available commands depend on the current implementation in the repository.

---

# Development Philosophy

Grisha is being developed incrementally.

The project focuses on building reliable low-level capabilities before moving toward higher-level autonomous behavior.

The current progression is:

```text
Terminal Assistant
        ↓
Command System
        ↓
System & Application Control
        ↓
Screen Observation
        ↓
Mouse & Keyboard Control
        ↓
Screen-Based Interaction
        ↓
Future GUI Understanding
        ↓
Future Voice Interaction
```

A key design principle is:

> **Keep internal data detailed, but keep user-facing responses concise.**

This will make the system suitable for both terminal interaction and future voice-based interaction.

---

# Current Status

## V1 — F1.18

**Completed.**

Grisha can now observe the Windows desktop, locate visible text through OCR, resolve matching elements, and interact with them using the mouse and keyboard.

The next major development stage will focus on improving the internal screen architecture and later adding deeper screen understanding.

---

# Future Direction

Planned future development includes areas such as:

- Better GUI element understanding
- Improved visual element identification
- More reliable button/input detection
- Spatial relationships between UI elements
- Screen state understanding
- Action verification
- Voice input/output
- More natural language commands
- Higher-level computer automation

These features are intentionally being developed step-by-step rather than treating the assistant as a single large system.

---

# Project Status

**Grisha V1 — F1.18 completed**

Built incrementally with Python on Windows.

