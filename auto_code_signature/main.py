# ---
# project: Codebase Signer
# file: main.py
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

import sys
import argparse
import tkinter as tk
import datetime
from typing import NoReturn
from utils import run_signer
from gui import SignerGUI


def main() -> None:
    """
    The main entry point for the Codebase Signer application.

    This function parses command-line arguments to determine whether to launch
    the Graphical User Interface (GUI) or run the signing process directly
    via the Command Line Interface (CLI).

    Arguments:
        --gui: Forces the launch of the Tkinter interface.
        --path: The directory containing files to be signed.
        --project: The name of the project for the YAML header.
        --author: The name of the author (defaults to medlav).
        --date: The creation date (defaults to current date).
        --license: The license type to apply (defaults to PRIVATE).
        --force-overwrite: Replace existing signatures if found.
        --merge-existing: Merge/Update existing signatures if found.
        --spdx: Default to False, adds a SPDX license on the header
    """
    parser = argparse.ArgumentParser(
        description="Codebase Signer: Inject YAML headers and licenses into source code."
    )

    # Mode Selection
    parser.add_argument(
        "--gui", action="store_true", help="Launch the graphical interface"
    )

    # CLI Arguments
    parser.add_argument("--path", type=str, help="Target directory to sign")
    parser.add_argument("--project", type=str, help="Name of the project")
    parser.add_argument("--author", type=str, default="medlav", help="Author name")
    parser.add_argument(
        "--date",
        type=str,
        default=datetime.date.today().strftime("%Y-%m-%d"),
        help="Creation date YYYY-MM-DD (default: today)",
    )
    parser.add_argument(
        "--license",
        type=str,
        default="PRIVATE",
        help="License type (MIT, PRIVATE, etc.)",
    )

    # New Signature Handling Flags
    parser.add_argument(
        "--force-overwrite",
        action="store_true",
        help="Overwrite existing YAML signatures",
    )
    parser.add_argument(
        "--merge-existing",
        action="store_true",
        help="Merge with/Update existing YAML signatures",
    )

    parser.add_argument(
        "--spdx",
        type=bool,
        default=False,
        help="Include SPDX license as header",
    )

    args = parser.parse_args()

    # Routing Logic
    if args.gui or len(sys.argv) == 1:
        print("Launching GUI...")
        root = tk.Tk()
        SignerGUI(root)
        root.mainloop()
    else:
        # Run CLI validation
        if not args.path or not args.project:
            handle_cli_error(parser)

        print(f"Starting CLI Signature Process for Project: {args.project}...")

        run_signer(
            target_path=args.path,
            author=args.author,
            license_type=args.license,
            project_name=args.project,
            created_date=args.date,
            overwrite=args.force_overwrite,
            merge=args.merge_existing,
            spdx=args.spdx,
        )


def handle_cli_error(parser: argparse.ArgumentParser) -> NoReturn:
    """
    Handles missing required CLI arguments by printing help and exiting.

    Args:
        parser: The active ArgumentParser instance.
    """
    print("\n[!] Error: CLI mode requires --path and --project.")
    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
