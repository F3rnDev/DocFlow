# -*- mode: python ; coding: utf-8 -*-
import os

script_dir = os.path.dirname(os.getcwd())

a = Analysis(
    ['launcher.py'],
    pathex=["C:\\Users\\lonel\\OneDrive\\Área de Trabalho\\Projetos Documentação\\DocFlow"],
    binaries=[],
    
    datas=[("assets/defaultIcon.png", "assets"),
        ("assets/nextFlowStep.png", "assets")
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
    name='launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='launcher',
)
