from distutils.core import setup
import py2exe

setup(
    options={'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows=[{
        'script': 'main.py',
        "icon_resources": [(0, "images/favicon.ico")],
    }
    ],
    zipfile=None,

)
