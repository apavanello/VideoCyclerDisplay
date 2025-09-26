# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('videoCycler', 'videoCycler'),
        ('db.sqlite3', '.'),
        ('staticfiles', 'staticfiles'),
        *collect_data_files('unfold', include_py_files=True),
        ],
    hiddenimports=[
        'videoCycler.apps',
        'unfold.contrib.filters.apps',
        'unfold.contrib.import_export.apps',
        'unfold.contrib.guardian.apps',
        'unfold.contrib.props.apps',
        'whitenoise.middleware',
        ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='VideoDisplay',
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
)
