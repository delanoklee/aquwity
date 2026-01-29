# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Acuity

import os
import sys

block_cipher = None

# Detect platform
is_macos = sys.platform == 'darwin'
is_windows = sys.platform == 'win32'

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
        'apscheduler.schedulers.background',
        'apscheduler.triggers.interval',
        'imagehash',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
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

if is_macos:
    # macOS: Create folder-based app bundle (recommended approach)
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='Acuity',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,  # UPX can cause issues on macOS
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=True,  # Required for macOS GUI apps
        target_arch=None,  # Build for host architecture
        codesign_identity=None,
        entitlements_file=None,
    )

    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=False,
        upx_exclude=[],
        name='Acuity',
    )

    app = BUNDLE(
        coll,
        name='Acuity.app',
        icon='assets/icon.icns.png' if os.path.exists('assets/icon.icns.png') else None,
        bundle_identifier='com.acuity.focustracker',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'LSMinimumSystemVersion': '10.13.0',
            'CFBundleShortVersionString': '1.0.3',
            'NSRequiresAquaSystemAppearance': 'False',  # Support dark mode
        },
    )
else:
    # Windows/Linux: Create single-file executable
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
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
    )
