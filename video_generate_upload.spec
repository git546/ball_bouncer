# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['video_generate_upload.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\\\Users\\\\SCHOOL\\\\Desktop\\\\ball_bouncer\\\\game_configurations.py', '.'), ('C:\\\\Users\\\\SCHOOL\\\\Desktop\\\\ball_bouncer\\\\FluidR3_GM.sf2', '.'), ('C:\\\\ffmpeg-2024-04-10-git-0e4dfa4709-full_build\\\\bin', 'ffmpeg'), ('C:\\\\fluidsynth-2.3.5-win10-x64\\\\bin', 'fluidsynth'), ('C:\\\\Users\\\\SCHOOL\\\\Desktop\\\\ball_bouncer\\\\client_secrets.json', '.')],
    hiddenimports=['cv2', 'numpy', 'pydub', 'music21', 'midi2audio', 'random', 'subprocess', 'ball_bounce', 'sound_ctl', 'game_configurations', 'uploader', 'pygame', 'google_auth_oauthlib', 'googleapiclient', 'googleapiclient.discovery', 'googleapiclient.http', 'googleapiclient.errors', 'google.auth'],
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
    name='video_generate_upload',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
