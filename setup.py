from cx_Freeze import setup, Executable

import constants
import environ
import imagepacker
import fileuploader

base = None
executables = [Executable("astrocam.py", base=base)]

packages = ["patool"]
buildOptions = dict(excludes=["tkinter"], includes=["idna.idnadata"],optimize=1)
setup(
    name = "astrocam",
    version = "0.1",
    description = "Astrocam utility",   
    executables = executables,
    options = dict(build_exe = buildOptions)
)
