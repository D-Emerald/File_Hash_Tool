# File Hash Tool

A lightweight, portable Python desktop application for quickly calculating, comparing and documenting cryptographic file hashes.

I created the **File Hash Tool** as a quick **pocket-access utility** for situations where I need to check a file hash without having to type out a command each time. While hashing a file through PowerShell or the command line is straightforward, repeatedly entering commands can become long and tedious when performing quick checks.

The GUI provides a simple alternative: **select or drag and drop a file, choose the algorithm, and click the button**.

The packaged executable can be kept on a USB drive, external storage or another convenient location and used when needed, without requiring Python to be installed.

The selected source file is processed **read-only**.

![File Hash Tool](images/File_Hash_Tool.png)

## Features

* Portable, ready-to-use Windows executable
* GUI-based file hashing without requiring command-line input
* Drag and drop file support
* Browse and select files
* Calculate an individual file hash
* Calculate all supported hashes
* MD5 selected by default
* Selectable hashing algorithms
* Verify a calculated hash against an expected hash
* Copy calculated hashes to the clipboard
* Display file name and file size
* Read-only source file processing
* Export a timestamped evidence record to the Windows Downloads folder
* Chunked file processing for handling larger files
* Python source code included for learning and modification

## Supported Hash Algorithms

### MD5

* MD5

### SHA-1

* SHA-1

### SHA-2

* SHA-224
* SHA-256
* SHA-384
* SHA-512

### SHA-3

* SHA3-224
* SHA3-256
* SHA3-384
* SHA3-512

### BLAKE2

* BLAKE2b
* BLAKE2s

## How It Works

1. Select a file using **Browse** or drag and drop it into the application.
2. Select a hashing algorithm.
3. Select **Calculate Hash** to generate the hash.
4. Use **Calculate All** to generate all supported hashes.
5. Enter an expected hash when verification is required.
6. Select **Verify Hash**.
7. The application reports whether the calculated value matches the expected value.
8. Export an evidence record when documentation is required.

The application reads the source file in **1 MB chunks**, allowing files to be processed without loading the entire file into memory.

## Hash Verification

Hash verification can be used to compare a calculated hash against a known expected value.

For example:

```text
Expected Hash:
65c400457612c4f0d8438bc86fa434e6

Calculated Hash:
65c400457612c4f0d8438bc86fa434e6

Result:
MATCH
```

The comparison is performed without modifying the source file.

## Evidence Record

The application can export a text-based evidence record to the user's Windows **Downloads** folder.

The record contains:

* File name
* File path
* File size
* Hash algorithm
* Calculated hash
* Expected hash, when provided
* Verification result
* Date and time
* Confirmation that the source file was processed read-only

This provides a quick way to document hash calculations during testing, file verification and other cybersecurity workflows.

## Example

The following image shows the MD5 hash generated for the application using PowerShell and provides an independent reference for verifying the application package.

![MD5 Hash](images/MD5-Hash.png)

**MD5:**

```text
65c400457612c4f0d8438bc86fa434e6
```

## Download and Use

A ready-to-use Windows executable is provided in:

```text
File_Hash_Tool.zip
```

Extract the ZIP archive and run:

```text
File_Hash_Tool.exe
```

No Python installation is required to use the packaged executable.

The ZIP makes the tool convenient to keep on a USB drive, external storage or another location for quick access when needed.

## Source Code

The Python source code is included in the main project directory:

```text
File_Hash_Tool.py
```

The source provides an example of building a practical desktop cybersecurity utility using Python, Tkinter, file handling and cryptographic hashing.

## Technologies

* Python
* Tkinter
* tkinterdnd2
* hashlib
* pathlib
* PyInstaller

## Running From Source

Python and the `tkinterdnd2` package are required.

Install the dependency:

```powershell
python -m pip install tkinterdnd2
```

Run the application:

```powershell
python File_Hash_Tool.py
```

## Building the Executable

The application can be packaged using **PyInstaller**.

The project includes a PyInstaller specification file for packaging the application and its required Tcl/Tk runtime components.

A typical build command is:

```powershell
python -m PyInstaller --clean File_Hash_Tool.spec
```

The resulting executable is created in:

```text
dist\File_Hash_Tool.exe
```

## Project Structure

```text
File_Hash_Tool/
│
├── File_Hash_Tool.py
├── File_Hash_Tool.spec
├── File_Hash_Tool.zip
│
└── images/
    ├── File_Hash_Tool.png
    └── MD5-Hash.png
```

### Project Files

**`File_Hash_Tool.py`**
Python source code for the application.

**`File_Hash_Tool.spec`**
PyInstaller configuration used to package the application and its required GUI runtime components.

**`File_Hash_Tool.zip`**
Ready-to-use packaged Windows executable.

**`images/File_Hash_Tool.png`**
Screenshot of the File Hash Tool graphical interface.

**`images/MD5-Hash.png`**
PowerShell screenshot showing the MD5 hash verification reference.
