import sys
import os
from cx_Freeze import setup, Executable

files = ['utils/', 'backend/', 'env/', 'data/']

target = Executable(
    script="App.py",
    base="Win32GUI"
)

setup(
    name="Peripheral Killing System",
    version = "0.1.2",
    description="Eleiminate the use of peripherals from your system",
    author = "Hardik Jaiswal", 
    options= {"build_exe": {'include_files':files}},
    executables= [target]
)