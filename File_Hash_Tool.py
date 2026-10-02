# -*- coding: utf-8 -*-
"""
File Hash Tool
---------------
Calculate, compare and document file hashes.

Features:
- Drag and drop files
- Browse for files
- Calculate individual hashes
- Calculate all supported hashes
- Verify an expected hash
- Copy hashes
- Export an evidence record
- Read-only file processing

Created on Fri Oct  2 14:53:38 2026

@author: devin
"""

import hashlib
import os
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from tkinterdnd2 import DND_FILES, TkinterDnD


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

CHUNK_SIZE = 1024 * 1024  # 1 MB

HASH_ALGORITHMS = {
    "MD5": "md5",
    "SHA-1": "sha1",
    "SHA-224": "sha224",
    "SHA-256": "sha256",
    "SHA-384": "sha384",
    "SHA-512": "sha512",
    "SHA3-224": "sha3_224",
    "SHA3-256": "sha3_256",
    "SHA3-384": "sha3_384",
    "SHA3-512": "sha3_512",
    "BLAKE2b": "blake2b",
    "BLAKE2s": "blake2s",
}


# ---------------------------------------------------------
# Hashing
# ---------------------------------------------------------

def calculate_hash(file_path, algorithm):
    """
    Calculate a hash for a file.

    The file is opened in read-only binary mode and
    processed in chunks so large files do not need to
    be loaded completely into memory.
    """

    hash_object = hashlib.new(algorithm)

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(CHUNK_SIZE)

            if not chunk:
                break

            hash_object.update(chunk)

    return hash_object.hexdigest()


def calculate_all_hashes(file_path):
    """
    Calculate all supported hashes in one pass through
    the file.
    """

    hash_objects = {
        name: hashlib.new(algorithm)
        for name, algorithm in HASH_ALGORITHMS.items()
    }

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(CHUNK_SIZE)

            if not chunk:
                break

            for hash_object in hash_objects.values():
                hash_object.update(chunk)

    return {
        name: hash_object.hexdigest()
        for name, hash_object in hash_objects.items()
    }


# ---------------------------------------------------------
# GUI Application
# ---------------------------------------------------------

class FileHashTool:

    def __init__(self, root):
        self.root = root

        self.root.title("File Hash Tool")
        self.root.geometry("720x850")
        self.root.minsize(650, 750)

        self.file_path = None
        self.current_hash = None
        self.current_algorithm = None
        self.all_hashes = {}

        self.create_variables()
        self.create_gui()

    # -----------------------------------------------------
    # Variables
    # -----------------------------------------------------

    def create_variables(self):

        self.file_name_var = tk.StringVar(
            value="No file selected"
        )

        self.file_size_var = tk.StringVar(
            value="File size: -"
        )

        self.algorithm_var = tk.StringVar(
            value="MD5"
        )

        self.hash_var = tk.StringVar()

        self.expected_hash_var = tk.StringVar()

    # -----------------------------------------------------
    # GUI
    # -----------------------------------------------------

    def create_gui(self):

        main = ttk.Frame(self.root, padding=15)
        main.pack(fill="both", expand=True)

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = ttk.Label(
            main,
            text="File Hash Tool",
            font=("Segoe UI", 20, "bold")
        )

        title.pack(pady=(0, 5))

        subtitle = ttk.Label(
            main,
            text="Calculate, verify and document file hashes"
        )

        subtitle.pack(pady=(0, 15))

        # -------------------------------------------------
        # File selection
        # -------------------------------------------------

        file_frame = ttk.LabelFrame(
            main,
            text="File"
        )

        file_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        drop_area = tk.Label(
            file_frame,
            text="Drag & Drop File Here\n\nor\n\nClick Browse",
            relief="groove",
            height=7,
            font=("Segoe UI", 11)
        )

        drop_area.pack(
            fill="x",
            padx=10,
            pady=10
        )

        drop_area.drop_target_register(DND_FILES)

        drop_area.dnd_bind(
            "<<Drop>>",
            self.handle_drop
        )

        browse_button = ttk.Button(
            file_frame,
            text="Browse",
            command=self.browse_file
        )

        browse_button.pack(pady=(0, 10))

        ttk.Label(
            file_frame,
            textvariable=self.file_name_var
        ).pack(
            anchor="w",
            padx=10
        )

        ttk.Label(
            file_frame,
            textvariable=self.file_size_var
        ).pack(
            anchor="w",
            padx=10,
            pady=(2, 10)
        )

        # -------------------------------------------------
        # Algorithm
        # -------------------------------------------------

        algorithm_frame = ttk.LabelFrame(
            main,
            text="Hash Algorithm"
        )

        algorithm_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        algorithm_row = ttk.Frame(
            algorithm_frame
        )

        algorithm_row.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            algorithm_row,
            text="Algorithm:"
        ).pack(side="left")

        algorithm_box = ttk.Combobox(
            algorithm_row,
            textvariable=self.algorithm_var,
            values=list(HASH_ALGORITHMS.keys()),
            state="readonly",
            width=20
        )

        algorithm_box.pack(
            side="left",
            padx=(10, 0)
        )

        # -------------------------------------------------
        # Hash buttons
        # -------------------------------------------------

        button_frame = ttk.Frame(main)

        button_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Button(
            button_frame,
            text="Calculate Hash",
            command=self.calculate_selected_hash
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 5)
        )

        ttk.Button(
            button_frame,
            text="Calculate All",
            command=self.calculate_all
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(5, 0)
        )

        # -------------------------------------------------
        # Hash result
        # -------------------------------------------------

        hash_frame = ttk.LabelFrame(
            main,
            text="Hash Result"
        )

        hash_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        hash_entry = ttk.Entry(
            hash_frame,
            textvariable=self.hash_var,
            state="readonly"
        )

        hash_entry.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Button(
            hash_frame,
            text="Copy Hash",
            command=self.copy_hash
        ).pack(
            pady=(0, 10)
        )

        # -------------------------------------------------
        # Verification
        # -------------------------------------------------

        verify_frame = ttk.LabelFrame(
            main,
            text="Verify Hash"
        )

        verify_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Label(
            verify_frame,
            text="Expected Hash:"
        ).pack(
            anchor="w",
            padx=10,
            pady=(10, 3)
        )

        expected_entry = ttk.Entry(
            verify_frame,
            textvariable=self.expected_hash_var
        )

        expected_entry.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        ttk.Button(
            verify_frame,
            text="Verify Hash",
            command=self.verify_hash
        ).pack(
            pady=(0, 10)
        )

        # -------------------------------------------------
        # Evidence
        # -------------------------------------------------

        evidence_frame = ttk.LabelFrame(
            main,
            text="Evidence"
        )

        evidence_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Button(
            evidence_frame,
            text="Export Evidence Record to Downloads",
            command=self.export_evidence
        ).pack(
            padx=10,
            pady=10,
            fill="x"
        )

        # -------------------------------------------------
        # Bottom buttons
        # -------------------------------------------------

        bottom_frame = ttk.Frame(main)

        bottom_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Button(
            bottom_frame,
            text="Clear",
            command=self.clear_all
        ).pack(
            side="left",
            expand=True,
            fill="x"
        )

    # -----------------------------------------------------
    # File handling
    # -----------------------------------------------------

    def browse_file(self):

        file_path = filedialog.askopenfilename()

        if file_path:
            self.load_file(file_path)

    def handle_drop(self, event):

        files = self.root.tk.splitlist(event.data)

        if not files:
            return

        file_path = files[0]

        if os.path.isfile(file_path):
            self.load_file(file_path)
        else:
            messagebox.showerror(
                "Invalid Selection",
                "Please drop a file, not a folder."
            )

    def load_file(self, file_path):

        self.file_path = file_path

        path = Path(file_path)

        self.file_name_var.set(
            f"File: {path.name}"
        )

        try:
            file_size = path.stat().st_size

            self.file_size_var.set(
                f"File size: {self.format_size(file_size)} "
                f"({file_size:,} bytes)"
            )

        except OSError as error:

            self.file_size_var.set(
                f"File size: Unable to read ({error})"
            )

        self.hash_var.set("")
        self.expected_hash_var.set("")

        self.current_hash = None
        self.current_algorithm = None
        self.all_hashes = {}

    # -----------------------------------------------------
    # Hash calculation
    # -----------------------------------------------------

    def calculate_selected_hash(self):

        if not self.file_path:
            messagebox.showwarning(
                "No File",
                "Please select or drag and drop a file first."
            )
            return

        algorithm_name = self.algorithm_var.get()
        algorithm = HASH_ALGORITHMS[algorithm_name]

        try:

            self.root.update_idletasks()

            result = calculate_hash(
                self.file_path,
                algorithm
            )

            self.current_hash = result
            self.current_algorithm = algorithm_name

            self.hash_var.set(result)

        except (OSError, ValueError) as error:

            messagebox.showerror(
                "Hash Error",
                f"Unable to calculate hash:\n\n{error}"
            )

    def calculate_all(self):

        if not self.file_path:
            messagebox.showwarning(
                "No File",
                "Please select or drag and drop a file first."
            )
            return

        try:

            self.root.update_idletasks()

            self.all_hashes = calculate_all_hashes(
                self.file_path
            )

            selected_algorithm = self.algorithm_var.get()

            self.current_hash = self.all_hashes[
                selected_algorithm
            ]

            self.current_algorithm = selected_algorithm

            self.hash_var.set(
                self.current_hash
            )

            self.show_all_hashes()

        except (OSError, ValueError) as error:

            messagebox.showerror(
                "Hash Error",
                f"Unable to calculate hashes:\n\n{error}"
            )

    def show_all_hashes(self):

        window = tk.Toplevel(self.root)

        window.title("All Hashes")
        window.geometry("750x500")
        window.minsize(600, 400)

        frame = ttk.Frame(
            window,
            padding=15
        )

        frame.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            frame,
            text="Hash Results",
            font=("Segoe UI", 14, "bold")
        ).pack(
            pady=(0, 10)
        )

        text = tk.Text(
            frame,
            wrap="word",
            font=("Consolas", 10)
        )

        text.pack(
            fill="both",
            expand=True
        )

        for name, result in self.all_hashes.items():

            text.insert(
                "end",
                f"{name}\n{result}\n\n"
            )

        text.config(state="disabled")

    # -----------------------------------------------------
    # Verification
    # -----------------------------------------------------

    def verify_hash(self):

        if not self.file_path:
            messagebox.showwarning(
                "No File",
                "Please select a file first."
            )
            return

        expected = self.expected_hash_var.get().strip()

        if not expected:
            messagebox.showwarning(
                "Missing Hash",
                "Enter the expected hash first."
            )
            return

        algorithm_name = self.algorithm_var.get()
        algorithm = HASH_ALGORITHMS[algorithm_name]

        try:

            self.root.update_idletasks()

            calculated = calculate_hash(
                self.file_path,
                algorithm
            )

            self.current_hash = calculated
            self.current_algorithm = algorithm_name

            self.hash_var.set(calculated)

            if calculated.lower() == expected.lower():

                messagebox.showinfo(
                    "Verification Result",
                    "HASH MATCH\n\n"
                    "The calculated hash matches "
                    "the expected hash."
                )

            else:

                messagebox.showwarning(
                    "Verification Result",
                    "HASH MISMATCH\n\n"
                    "The calculated hash does not "
                    "match the expected hash."
                )

        except (OSError, ValueError) as error:

            messagebox.showerror(
                "Verification Error",
                f"Unable to verify file:\n\n{error}"
            )

    # -----------------------------------------------------
    # Clipboard
    # -----------------------------------------------------

    def copy_hash(self):

        value = self.hash_var.get()

        if not value:
            messagebox.showwarning(
                "No Hash",
                "There is no hash to copy."
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(value)

    # -----------------------------------------------------
    # Evidence export
    # -----------------------------------------------------

    def export_evidence(self):

        if not self.file_path:
            messagebox.showwarning(
                "No File",
                "Please select a file first."
            )
            return

        if not self.current_hash:
            messagebox.showwarning(
                "No Hash",
                "Calculate a hash before exporting "
                "an evidence record."
            )
            return

        try:

            path = Path(self.file_path)

            file_size = path.stat().st_size

            timestamp = datetime.now()

            expected = self.expected_hash_var.get().strip()

            if expected:

                if (
                    self.current_hash.lower()
                    == expected.lower()
                ):
                    verification = "MATCH"
                else:
                    verification = "MISMATCH"

            else:

                verification = "Not performed"

            report = (
                "FILE HASH EVIDENCE RECORD\n"
                "=========================\n\n"
                f"File Name: {path.name}\n"
                f"File Path: {path}\n"
                f"File Size: {file_size:,} bytes\n\n"
                f"Hash Algorithm: "
                f"{self.current_algorithm}\n\n"
                f"Calculated Hash:\n"
                f"{self.current_hash}\n\n"
                f"Expected Hash:\n"
                f"{expected if expected else 'Not provided'}\n\n"
                f"Verification:\n"
                f"{verification}\n\n"
                f"Date and Time:\n"
                f"{timestamp.strftime('%d/%m/%Y %H:%M:%S')}\n\n"
                "Source File:\n"
                "Read-only processing\n"
            )

            downloads = Path.home() / "Downloads"

            downloads.mkdir(
                parents=True,
                exist_ok=True
            )

            filename = (
                f"FileHash_Evidence_"
                f"{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
            )

            output_path = downloads / filename

            with open(
                output_path,
                "w",
                encoding="utf-8"
            ) as report_file:

                report_file.write(report)

            messagebox.showinfo(
                "Evidence Exported",
                f"Evidence record saved to:\n\n"
                f"{output_path}"
            )

        except OSError as error:

            messagebox.showerror(
                "Export Error",
                f"Unable to create evidence record:\n\n{error}"
            )

    # -----------------------------------------------------
    # Clear
    # -----------------------------------------------------

    def clear_all(self):

        self.file_path = None
        self.current_hash = None
        self.current_algorithm = None
        self.all_hashes = {}

        self.file_name_var.set(
            "No file selected"
        )

        self.file_size_var.set(
            "File size: -"
        )

        self.hash_var.set("")
        self.expected_hash_var.set("")

        self.algorithm_var.set("MD5")

    # -----------------------------------------------------
    # Utilities
    # -----------------------------------------------------

    @staticmethod
    def format_size(size):

        units = [
            "bytes",
            "KB",
            "MB",
            "GB",
            "TB"
        ]

        value = float(size)

        for unit in units:

            if value < 1024 or unit == "TB":
                return f"{value:.2f} {unit}"

            value /= 1024


# ---------------------------------------------------------
# Start Application
# ---------------------------------------------------------

if __name__ == "__main__":

    root = TkinterDnD.Tk()

    app = FileHashTool(root)

    root.mainloop()

