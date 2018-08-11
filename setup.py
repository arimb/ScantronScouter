from cx_Freeze import setup, Executable

base = None

executables = [Executable("ScantronScouter.py", base=base)]

packages = ["cv2", "numpy", "math", "configparser", "pathlib", "sys", "tkinter"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "ScantronScouter.exe",
    options = options,
    version = "1.0",
    description = 'Semi-paperless FRC scouting app',
    executables = executables
)