import sys
from cx_Freeze import setup, Executable

setup(name = "Coronabi",
      version = "0.1",
      description = "My GUI App",
      executables = [Executable("GUI.py")])