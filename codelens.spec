# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/themes/*.qss', 'assets/themes'),
        ('assets/icons/*', 'assets/icons'),
    ],
    hiddenimports=[
        'google.generativeai',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'keyring.backends',
        'keyring.backends.Windows',
        'keyring.backends.macOS',
        'keyring.backends.SecretService',
        'markdown',
        'pygments',
        'reportlab',
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
    name='CodeLens',
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
    icon='assets/icons/app_icon.ico' if os.path.exists('assets/icons/app_icon.ico') else None,
)

# macOS app bundle
app = BUNDLE(
    exe,
    name='CodeLens.app',
    icon='assets/icons/app_icon.icns' if os.path.exists('assets/icons/app_icon.icns') else None,
    bundle_identifier='com.codelens.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
    },
)
