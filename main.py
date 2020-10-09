import sys
from Windows.main import winget
from Linux.main import sudo

def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    platform = platforms[sys.platform]
    return platform

TOKEN = "NzUwMzY4OTAxNDYzODAxOTg3.X05hfw.lpe0ZE6xE26K05hG-Q9C3Luixto"

platform = get_platform()
if platform == "Windows":
    winget(TOKEN)
elif platform == "Linux":
    sudo(TOKEN)