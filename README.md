
# Codebase Signer

**Version:** 0.0.3.0

**Date:** 05-02-2026

A simple utility to help inject, update, and manage YAML-formatted metadata headers and open-source licenses within Python projects.

**Note:** This is a hobby project built to be as lightweight as possible. It has **zero external dependencies** and runs entirely on the Python standard library.

## Features

* **No Dependencies**: Runs out-of-the-box with any standard Python installation.
* **Standard Compliance**: Injects signatures as module-level docstrings or `#` comments, respecting PEP 8.
* **SPDX Support**: Optionally include [SPDX-License-Identifiers](https://spdx.org/licenses/) for license scanning tools.
* **Shebang Preservation**: Automatically detects `#!` lines and inserts headers immediately after them.
* **Intelligent Detection**: Scans files to prevent double-signing by checking for YAML markers (`---`).
* **Flexible Updates**: Supports overwriting or merging existing signatures through CLI flags or GUI toggles.
* **Batch Processing**: Recursively walks through directories while excluding common folders like `.git`, `venv`, and `__pycache__`.

---

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/medlav/codebase-signer.git
cd codebase-signer

```

2. **Run it**:
Since there are no dependencies to install, you can run the tool immediately using Python. No `pip install` or virtual environments required.

---

## Usage

The script detects how it is being called. Running without arguments launches a simple **GUI**, while adding arguments triggers the **CLI**.

### 1. Graphical User Interface (GUI)

Simply run the script to open the window:

```bash
python main.py

```

**GUI Options:**

* **Directory Browser**: Select your project folder.
* **Metadata Fields**: Define Project Name, Author, and Creation Date.
* **Sign Options**:
* **Force Overwrite**: Replaces existing signatures entirely.
* **Merge Existing**: Updates metadata while preserving the file structure.
* **Add SPDX**: Includes the standard `SPDX-License-Identifier` line.
* **Use # Comments**: Uses comment blocks instead of triple-quoted docstrings.



### 2. Command Line Interface (CLI)

For quick tasks or automation:

```bash
python main.py --path ./my_project --project "My Project" --author "medlav" --license MIT --spdx

```

#### CLI Arguments Reference:

| Argument | Description | Default |
| --- | --- | --- |
| `--path` | Directory containing files to sign | `.` |
| `--project` | Name of the project | `My Project` |
| `--author` | Author name | `medlav` |
| `--license` | License key (MIT, Apache-2.0, etc.) | `PRIVATE` |
| `--force-overwrite` | Replace existing signatures | `False` |
| `--merge-existing` | Update existing metadata | `False` |
| `--spdx` | Include SPDX identifier | `False` |
| `--as-comment` | Use `#` instead of `"""` | `False` |

---

## Signature Structure

The tool generates a header structured like this:

```python
# SPDX-License-Identifier: MIT
# Copyright (C) 2026 medlav
"""
---
project: My Project
file: main.py
author: medlav
created: 2026-02-05
license: MIT
---
[Full License Text Appears Here]
"""

import os
# ... rest of code

```

---

## Create your own Executable (.exe)

If you want to use this as a standalone Windows app, you can convert it using `auto-py-to-exe`.

1. **Install the converter**: `pip install auto-py-to-exe`
2. **Launch it**: `auto-py-to-exe`
3. **Configuration**:
* **Script Location**: Select `main.py`.
* **Onefile**: Select "One File" for a single portable `.exe`.
* **Window Based**: Select "Window Based" to hide the console.
* **Additional Files**: Make sure to add `utils.py`, `licenses.py`, and `spdx_licenses.csv`.


4. **Click Convert**.

---

## Credits

* Inspired by [python-license](https://pypi.org/project/python-license/).
* License data sourced from [SPDX](https://spdx.org/licenses/).

---
