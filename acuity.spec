# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Acuity

import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.env.example', '.'),
    ],
    hiddenimports=[
        'anthropic',
        'PIL',
        'PIL._tkinter_finder',
        'mss',
        'dotenv',
        'apscheduler',
        'imagehash',
        'tkinter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Acuity',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,  # Windows icon
)

# For macOS, create an app bundle
app = BUNDLE(
    exe,
    name='Acuity.app',
    icon='assets/icon.icns.png' if os.path.exists('assets/icon.icns.png') else None,
    bundle_identifier='com.acuity.focustracker',
)
