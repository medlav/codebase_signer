# ---
# project: Codebase Signer
# file: gui.py
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

from tkinter import BooleanVar, StringVar, Tk, filedialog, messagebox, ttk
import os
import sys
import argparse
import datetime
from utils import run_signer


class SignerGUI:
    """
    A Tkinter-based graphical user interface for the Codebase Signer utility.

    Provides fields for project metadata and checkboxes for configuration
    toggles like SPDX headers and comment styles.
    """

    def __init__(self, root):
        """
        Initializes the GUI components and variables.

        Args:
            root: The Tkinter root window instance.
        """
        self.root = root
        self.root.title("Codebase Signer")
        self.root.geometry("600x700")  # Increased height slightly for new options
        self.root.resizable(True, True)

        # Variables
        self.target_path = StringVar(value=os.getcwd())
        self.project_name = StringVar(value="My Project")
        self.author_name = StringVar(value="medlav")
        self.creation_date = StringVar(value=datetime.date.today().strftime("%Y-%m-%d"))
        self.license_var = StringVar(value="PRIVATE")

        # New Toggle Variables
        self.overwrite_var = BooleanVar(value=False)
        self.merge_var = BooleanVar(value=False)
        self.spdx_var = BooleanVar(value=False)
        self.spdx_only_var = BooleanVar(value=False)
        self.as_comment_var = BooleanVar(value=False)

        self.license_options = [
            "Unlicense",
            "PRIVATE",
            "MIT",
            "BSD-3-Clause",
            "Apache-2.0",
            "GPL-3.0-or-later",
            "GPL-2.0-or-later",
            "AGPL-3.0",
            "LGPL-3.0-or-later",
        ]

        self.setup_ui()

    def setup_ui(self):
        """
        Builds the graphical components of the application.

        Sets up entry fields for metadata and a labeled frame for
        configuration toggles.
        """
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame, text="Codebase Signer", font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        # Project Name
        ttk.Label(main_frame, text="Project Name:").pack(anchor="w")
        ttk.Entry(main_frame, textvariable=self.project_name).pack(fill="x", pady=5)

        # Path Selection
        ttk.Label(main_frame, text="Project Directory:").pack(anchor="w", pady=(10, 0))
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill="x", pady=5)
        ttk.Entry(path_frame, textvariable=self.target_path).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(path_frame, text="Browse", command=self.browse_folder).pack(
            side="right", padx=5
        )

        # Author Input
        ttk.Label(main_frame, text="Author Name:").pack(anchor="w", pady=(10, 0))
        ttk.Entry(main_frame, textvariable=self.author_name).pack(fill="x", pady=5)

        # Creation Date Input
        ttk.Label(main_frame, text="Creation Date (YYYY-MM-DD):").pack(
            anchor="w", pady=(10, 0)
        )
        ttk.Entry(main_frame, textvariable=self.creation_date).pack(fill="x", pady=5)

        # License Dropdown
        ttk.Label(main_frame, text="Select License:").pack(anchor="w", pady=(10, 0))
        license_cb = ttk.Combobox(
            main_frame,
            textvariable=self.license_var,
            values=self.license_options,
            state="readonly",
        )
        license_cb.pack(fill="x", pady=5)

        # Options Frame (Overwrite & Merge)
        options_frame = ttk.LabelFrame(main_frame, text="Sign Options", padding="10")
        options_frame.pack(fill="x", pady=(15, 0))

        ttk.Checkbutton(
            options_frame,
            text="Force Overwrite existing signature",
            variable=self.overwrite_var,
        ).pack(anchor="w")

        ttk.Checkbutton(
            options_frame,
            text="Merge with existing signature",
            variable=self.merge_var,
        ).pack(anchor="w")

        ttk.Checkbutton(
            options_frame,
            text="Add SPDX lincense with signature",
            variable=self.spdx_var,
        ).pack(anchor="w")

        ttk.Checkbutton(
            options_frame,
            text="SPDX Only (No metadata/license text)",
            variable=self.spdx_only_var,
        ).pack(anchor="w")

        ttk.Checkbutton(
            options_frame,
            text='Use # comments instead of triple quotes """',
            variable=self.as_comment_var,
        ).pack(anchor="w")

        # Run Button
        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=20)
        run_btn = ttk.Button(
            main_frame, text="START SIGNING", command=self.execute_signing
        )
        run_btn.pack(fill="x", ipady=10)

    def browse_folder(self):
        """
        Opens a native directory selection dialog and updates the target path.
        """
        selected = filedialog.askdirectory()
        if selected:
            self.target_path.set(selected)

    def execute_signing(self):
        """
        Collects values from the GUI variables and triggers the run_signer logic.

        Displays a success message box on completion or an error box on failure.
        """
        try:
            run_signer(
                target_path=self.target_path.get(),
                author=self.author_name.get(),
                license_type=self.license_var.get(),
                project_name=self.project_name.get(),
                created_date=self.creation_date.get(),
                overwrite=self.overwrite_var.get(),
                merge=self.merge_var.get(),
                spdx=self.spdx_var.get(),
                spdx_only=self.spdx_only_var.get(),  # New
                as_comment=self.as_comment_var.get(),  # New
            )
            messagebox.showinfo("Success", "Files processed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    """
    Application entry point. Launches the GUI if no arguments are provided,
    otherwise parses CLI arguments to run in headless mode.
    """
    parser = argparse.ArgumentParser(description="Sign codebase with YAML headers.")
    parser.add_argument("--path", help="Directory to sign")
    parser.add_argument("--project", help="Project name")
    parser.add_argument("--author", help="Author name")
    parser.add_argument("--license", help="License type")
    parser.add_argument("--date", help="Creation date (YYYY-MM-DD)")
    parser.add_argument(
        "--force-overwrite", action="store_true", help="Overwrite existing signatures"
    )
    parser.add_argument(
        "--merge-existing", action="store_true", help="Merge existing signatures"
    )
    parser.add_argument("--spdx", help="Merge existing signatures")

    if len(sys.argv) == 1:
        root = Tk()
        SignerGUI(root)
        root.mainloop()
    else:
        parser.add_argument("--spdx-only", action="store_true")
        parser.add_argument("--as-comment", action="store_true")
        parser.add_argument("--spdx", action="store_true")

        args = parser.parse_args()
        default_date = datetime.date.today().strftime("%Y-%m-%d")

        run_signer(
            target_path=args.path or ".",
            author=args.author or "Author",
            license_type=args.license or "PRIVATE",
            project_name=args.project or "Project",
            created_date=args.date or default_date,
            overwrite=args.force_overwrite,
            merge=args.merge_existing,
            spdx=args.spdx,
            spdx_only=args.spdx_only,
            as_comment=args.as_comment,
        )


if __name__ == "__main__":
    main()
