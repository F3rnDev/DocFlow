# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    
    datas=[("assets/defaultIcon.png", "assets"),
        ("assets/nextFlowStep.png", "assets"),
        ("assets/down-arrow.svg", "assets"),
        ("assets/flags/por.svg", "assets/flags"),
        ("assets/flags/spa.svg", "assets/flags"),
        ("assets/flags/eng.svg", "assets/flags"),
    ],

    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DocFlow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DocFlow',
)
