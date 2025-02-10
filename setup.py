import sys
from cx_Freeze import setup, Executable

# 依赖项
build_exe_options = {
    "packages": ["os", "tkinter", "json", "datetime", "sys", "pygame"],
    "excludes": ["tkinter.test", "unittest"],
    "include_files": [
        "quotes.json",
        "README.md",
        "LICENSE.txt",
        "icon.svg",
        "mytarget.ico"
    ],
    "optimize": 2,
}

# 基本信息
setup(
    name="MyTarget",
    version="1.0.5",
    description="MyTarget目标管理器",
    author="A先生",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base="Win32GUI",
            target_name="MyTarget.exe",
            icon="mytarget.ico",
            copyright="Copyright (C) 2023-2024 A先生",
        )
    ],
) 