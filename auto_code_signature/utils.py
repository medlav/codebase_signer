# ---
# project: Codebase Signer
# file: utils.py
# author: medlav
# created: 2026-02-05
# license: BSD-3-CLAUSE
# ---
# Copyright (c) 2026 medlav
#
# This is free software, this software was made as a custom private solution.
# The code and derived executables and binaries are meant to be used only privately.
# The following code is not meant to be shared as open source or free software.
# If this code is shared publicly for research, audit or teaching purposes
# it should be considered as Unlicensed code.
#
# THE AUTHOR IS NOT LIABLE FOR ANY MISUSE OF THE CODE.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import csv
import os
import datetime
from typing import Set, Dict, Callable
from licenses import (
    get_private_use_license,
    get_mit_license,
    get_apache_license,
    get_bsd_3_clause,
    get_gpl_v3,
    get_agpl_v3,
    get_lgpl_v3,
    get_gpl_v2,
    get_unlicense_license,
)

# --- CONFIGURATION ---
EXTENSIONS: Set[str] = {".py"}
EXCLUDE_DIRS: Set[str] = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "env",
    ".env",
    "build",
    "dist",
    "auto_signature",
}


def get_spdx_license_key(license_key: str) -> str:
    """
    Legge spdx_licenses.csv e cerca il match esatto nella colonna Identifier.
    """
    file_path = "spdx_licenses.csv"

    if not os.path.exists(file_path):
        return license_key

    with open(file_path, mode="r", encoding="utf-8") as f:
        # Usiamo csv.reader per scansionare il file
        spdx_licenses_csv = csv.reader(f)

        # Saltiamo l'header
        next(spdx_licenses_csv, None)

        for row in spdx_licenses_csv:
            identifier = row[1]  # Seconda colonna: Identifier
            if identifier == license_key:
                return identifier

    # Se non trova il match esatto, restituisce il parametro in ingresso
    return license_key


def generate_spdx_header(
    filename: str, author: str, license_key: str, years: str
) -> str:
    """
    Internal helper to generate the SPDX and Copyright comment block.

    Args:
        filename: Name of the file being signed.
        author: Name of the creator.
        license_key: TODO deprecate this soon, only accept this licenses for now
        spdx_license_key: The short-code for the license must be exactly one of the following.
        project_name: Name of the project.
        created_date: The date string provided by the user or default.

    Returns:
        A formatted string containing the YAML block and license text.
    """
    # Map extensions to (prefix, suffix, is_block_style)
    # Using the formats you specified for py, js, ts, c, h, css, html
    styles = {
        ".py": ("# ", ""),
        ".js": ("// ", ""),
        ".jsx": ("// ", ""),
        ".ts": ("// ", ""),
        ".tsx": ("// ", ""),
        ".c": ("// ", ""),
        ".h": ("// ", ""),
        ".css": ("/* ", " */"),
        ".html": ("/* ", " */"),
    }

    _, ext = os.path.splitext(filename.lower())

    # Default to '#' if extension not explicitly supported, or skip
    if ext not in styles:
        return ""

    prefix, suffix = styles[ext]

    license_key = get_spdx_license_key(license_key=license_key)

    line1 = f"{prefix}SPDX-License-Identifier: {license_key}{suffix}"
    line2 = f"{prefix}Copyright (C) {years}  {author}{suffix}"

    return f"{line1}\n{line2}\n"


def generate_header(
    filename: str,
    author: str,
    license_key: str,
    project_name: str,
    created_date: str | None = None,
    spdx: bool = False,
    spdx_only: bool = False,
    as_comment: bool = False,
) -> str:
    """
    Generates a YAML-formatted header string inside a Python docstring.

    Args:
        filename: Name of the file being signed.
        author: Name of the creator.
        license_key: The short-code for the license (e.g., 'MIT').
        project_name: Name of the project.
        created_date: The date string provided by the user or default.

    Returns:
        A formatted string containing the YAML block and license text.
    """

    if created_date is None:
        created_date = datetime.date.today().strftime("%Y-%m-%d")

    year = datetime.datetime.now().year

    licenses: Dict[str, Callable[[int, str], str]] = {
        "Unlicense": get_unlicense_license,
        "PRIVATE": get_private_use_license,
        "MIT": get_mit_license,
        "BSD-3-Clause": get_bsd_3_clause,
        "Apache-2.0": get_apache_license,
        "GPL-3.0-or-later": get_gpl_v3,
        "GPL-2.0-or-later": get_gpl_v2,
        "AGPL-3.0": get_agpl_v3,
        "LGPL-3.0-or-later": get_lgpl_v3,
    }

    key = license_key.upper().strip()
    license_func = licenses.get(key, get_private_use_license)
    license_text = license_func(year, author)

    spdx_header = ""
    if spdx or spdx_only:
        spdx_header = generate_spdx_header(
            filename=filename,
            author=author,
            license_key=license_key,
            years=str(year),
        )

    if spdx_only:
        return spdx_header

    header = (
        f"---\n"
        f"project: {project_name}\n"
        f"file: {filename}\n"
        f"author: {author}\n"
        f"created: {created_date}\n"
        f"license: {key}\n"
        f"---\n"
        f"{license_text.strip()}"
    )

    if as_comment:
        lines = header.splitlines()
        commented_lines = []
        for line in lines:
            clean_line = line.strip()
            if clean_line.startswith("#"):
                commented_lines.append(clean_line)
            else:
                commented_lines.append(f"# {line}")
        return f"{spdx_header}{'\n'.join(commented_lines)}\n"
    else:
        # Default: Docstring style
        return f'{spdx_header}\n"""\n{header}\n"""\n'


def is_already_signed(file_path: str) -> tuple[bool, int, int]:
    """
    Analyzes the beginning of a Python file to determine if it is already signed.

    The function scans the file line-by-line, ignoring leading whitespace,
    shebangs, and comments. It stops execution as soon as it encounters
    actual code (like an import) or a triple-quoted docstring.

    Args:
        file_path (str): The path to the .py file to check.

    Returns:
        Tuple[bool, int, int]: (is_signed, start_line_index, end_line_index)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        in_docstring = False
        quote_symbol = None
        start_idx = -1

        for i, line in enumerate(lines):
            stripped = line.strip()

            if not stripped:
                continue

            # --- CASE 1: COMMENT STYLE SIGNATURE (# ---) ---
            if not in_docstring and stripped.startswith("# ---"):
                scan_limit = min(i + 100, len(lines))  # Scan deeper for license text
                found_license = False
                end_metadata_idx = -1

                # Step A: Find the end of the YAML block
                for j in range(i, scan_limit):
                    if "license:" in lines[j].lower():
                        found_license = True
                    if j > i and lines[j].strip() == "# ---":
                        end_metadata_idx = j
                        break

                if found_license and end_metadata_idx != -1:
                    # Step B: Greedy Scan. Eat all consecutive # comments after the block
                    # This captures the license text that was left behind before.
                    final_end = end_metadata_idx
                    for k in range(end_metadata_idx + 1, len(lines)):
                        if lines[k].strip().startswith("#") or not lines[k].strip():
                            final_end = k
                        else:
                            break  # Hit code (import, def, etc.)

                    # Step C: Check for SPDX above
                    final_start = i
                    if i > 0 and "SPDX-License-Identifier" in lines[i - 1]:
                        final_start = i - 1
                    elif i > 1 and "SPDX-License-Identifier" in lines[i - 2]:
                        final_start = i - 2

                    return True, final_start, final_end

            # Skip standard comments/shebangs if we haven't hit a block yet
            if stripped.startswith(("#", "#!")):
                continue

            # --- CASE 2: DOCSTRING STYLE SIGNATURE (""") ---
            if not in_docstring:
                if stripped.startswith(('"""', "'''")):
                    in_docstring = True
                    quote_symbol = '"""' if stripped.startswith('"""') else "'''"
                    start_idx = i
                    if stripped.count(quote_symbol) == 2 and len(stripped) > 3:
                        if "---" in stripped and "license:" in stripped:
                            final_start = i
                            if i > 0 and "SPDX-License-Identifier" in lines[i - 1]:
                                final_start = i - 1
                            return True, final_start, i
                    continue
            else:
                if quote_symbol in stripped:  # type: ignore
                    full_text = "".join(lines[start_idx : i + 1])
                    if "---" in full_text and "license:" in full_text:
                        final_start = start_idx
                        if (
                            start_idx > 0
                            and "SPDX-License-Identifier" in lines[start_idx - 1]
                        ):
                            final_start = start_idx - 1
                        return True, final_start, i
                    in_docstring = False

            # If we hit real code, stop looking
            if stripped and not stripped.startswith(("#", '"""', "'''")):
                break

    except Exception as e:
        print(f"[!] Error reading {file_path}: {e}")

    return False, -1, -1


def inject_signature(
    file_path: str,
    author: str,
    license_type: str,
    project_name: str,
    created_date: str | None = None,
    spdx: bool = False,
    overwrite: bool = False,
    merge: bool = False,
    spdx_only: bool = False,
    as_comment: bool = False,
) -> None:
    """
    Injects a YAML metadata header and license text into a specific file.

    This function reads the file, generates a header based on provided metadata,
    and prepends it to the file content. It respects shebang lines (#!...) by
    inserting the signature immediately after them.

    Args:
        file_path (str): Absolute or relative path to the file.
        author (str): Name of the author.
        license_type (str): The license key (e.g., 'MIT').
        project_name (str): Name of the project.
        created_date (str): Date string in YYYY-MM-DD format.
        overwrite (bool): If True, replaces existing signature.
        merge (bool): If True, replaces existing signature (merge logic).
    """
    filename = os.path.basename(file_path)

    # Single scan to get signature status and coordinates
    already_signed, start_line, end_line = is_already_signed(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Skipping {file_path}: {e}")
        return

    if already_signed:
        if not overwrite and not merge:
            print(
                f"[-] Already signed: {filename}\n\tSkipping file: "
                f"\nIf you want to overwrite the existing signature add --force-overwrite "
                f"\nIf you want to merge with the existing signature add --merge-existing"
            )
            return

        # Remove existing signature lines if we are overwriting or merging
        lines = lines[:start_line] + lines[end_line + 1 :]

        if merge:
            print(
                f"[-] Already signed: {filename}\n\t--merge-existing selected: merging signature"
            )
        elif overwrite:
            print(
                f"[-] Already signed: {filename}\n\t--force-overwrite selected: overwriting signature"
            )

    full_header = generate_header(
        filename,
        author,
        license_type,
        project_name,
        created_date,
        spdx,
        spdx_only,
        as_comment,
    )

    # Logic to insert after Shebang or at top
    if lines and lines[0].startswith("#!"):
        shebang = lines[0] if lines[0].endswith("\n") else lines[0] + "\n"
        new_content = shebang + "\n" + full_header + "\n" + "".join(lines[1:])
    else:
        new_content = full_header + "\n" + "".join(lines)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[+] Signed: {file_path}")


def run_signer(
    target_path: str,
    author: str,
    license_type: str,
    project_name: str,
    created_date: str | None = None,
    spdx: bool = False,
    overwrite: bool = False,
    merge: bool = False,
    spdx_only: bool = False,
    as_comment: bool = False,
) -> None:
    """
    Walks through the directory tree and applies signatures to supported files.

    Args:
        target_path: The root directory to start scanning.
        author: Name of the author.
        license_type: The license identifier.
        project_name: Name of the project.
        created_date: Optional creation date string.
        spdx: Whether to include SPDX headers.
        overwrite: Overwrite existing signatures.
        merge: Merge with existing signatures.
        spdx_only: Only generate the SPDX line.
        as_comment: Use comment syntax instead of docstrings.
    Returns:
        None (this is a callable, it simply runs the signature script for every file in the selected folder)
    """
    target_abs = os.path.abspath(target_path)
    print(f"Starting auto-signature on: {target_abs}")

    if not os.path.exists(target_abs):
        print(f"Error: Path {target_abs} not found.")
        return

    for root, dirs, files in os.walk(target_abs):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                file_path = os.path.join(root, file)
                inject_signature(
                    file_path,
                    author,
                    license_type,
                    project_name,
                    created_date,
                    spdx,
                    overwrite,
                    merge,
                    spdx_only,
                    as_comment,
                )


def run_cli() -> None:
    """
    Parses command-line arguments and executes the signing process.
    """
    parser = argparse.ArgumentParser(
        description="Sign codebase with YAML headers and license text."
    )

    parser.add_argument("--path", default=".", help="Directory to sign")
    parser.add_argument("--project", default="My Project", help="Project name")
    parser.add_argument("--author", default="medlav", help="Author name")
    parser.add_argument(
        "--date", default=datetime.date.today().strftime("%Y-%m-%d"), help="YYYY-MM-DD"
    )
    parser.add_argument("--license", default="PRIVATE", help="License type")

    # Restored flags for overwrite and merge
    parser.add_argument(
        "--force-overwrite", action="store_true", help="Overwrite existing signatures"
    )
    parser.add_argument(
        "--merge-existing", action="store_true", help="Merge/Update existing signatures"
    )

    args = parser.parse_args()

    run_signer(
        target_path=args.path,
        author=args.author,
        license_type=args.license,
        project_name=args.project,
        created_date=args.date,
        overwrite=args.force_overwrite,
        merge=args.merge_existing,
    )
