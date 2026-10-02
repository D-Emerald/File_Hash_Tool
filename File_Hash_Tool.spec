a = Analysis(
    ["File_Hash_Tool.py"],
    pathex=[],
    binaries=[
        (r"C:\Users\devin\anaconda3\Library\bin\tcl86t.dll", "."),
        (r"C:\Users\devin\anaconda3\Library\bin\tk86t.dll", "."),
    ],
    datas=[
        (r"C:\Users\devin\anaconda3\Library\lib\tcl8.6", "tcl8.6"),
        (r"C:\Users\devin\anaconda3\Library\lib\tk8.6", "tk8.6"),
    ],
    hiddenimports=[
        "tkinter",
        "tkinterdnd2",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="File_Hash_Tool",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)