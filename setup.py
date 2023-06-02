from setuptools import setup

APP = ['main.py']
DATA_FILES = ['assets', 'graphics']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleName': 'Connect 5ive',
        'CFBundleDisplayName': 'Connect 5ive',
        'CFBundleGetInfoString': 'Connect 5ive',
        'CFBundleExecutable': 'Connect 5ive',
        'CFBundleIdentifier': 'com.yourcompany.connect5ive',
        'LSMinimumSystemVersion': '10.9.0',
    },
    'packages': ['pygame'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
