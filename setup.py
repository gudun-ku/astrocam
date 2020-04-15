from cx_Freeze import setup, Executable

import constants
import environ
import imagepacker
import fileuploader

PROGRAM_NAME = "Astrocam utility"
VERSION = "0.1.3"
AUTHOR = "Aleks Beloushkin gudun.ku@gmail.com"


base = None
executables = [Executable("astrocam.py", base=base)]

packages = ["patool"]
buildOptions = dict(excludes=["tkinter","sqlite"], includes=["idna.idnadata","re"],optimize=1)
setup(
    name = PROGRAM_NAME,
    version = VERSION,
    author = AUTHOR,
    description = "Astrocam utility program to pack and send astrophoto",   
    executables = executables,
    options = dict(build_exe = buildOptions)
)
