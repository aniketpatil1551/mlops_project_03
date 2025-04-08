## -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis

block_cipher = None

a = Analysis(
    ['manage.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('secret_key.txt', '.'),
        ('./venv/Lib/site-packages/', '.'),
        ('./app', 'app'),
        ('./aluminiumapp/mlscripts/*.h5', 'aluminiumapp/mlscripts/'), # Include your Django app
    ],
    hiddenimports=[
        'django',
        'django.core.management',
        'django.core.management.commands',
        'django.core.management.commands.runserver',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'autograd',
        'autograd.numpy',
        'autograd.numpy.numpy_boxes',
        'autograd.numpy.numpy_vspaces',
        # Add any other Django apps or third-party packages you're using
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SciDentAI-server',
    exclude_source_files=True,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    #console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SciDentAI-server',
    exclude_source_files=True
)


#trial
# -*- mode: python ; coding: utf-8 -*-
#import PyInstaller.config
#PyInstaller.config.CONF['distpath'] = "."
#import os
#import sys
#
#a = Analysis(
#    ['manage.py'],
#    pathex=[],
#    binaries=[],
#    datas=[
#        ('secret_key.txt', '.'),
#        ('./venv/Lib/site-packages/', '.'),
#        ('app', '.'),  # Include your Django app
#    ],
#    hiddenimports=[
#        'django',
#        'django.core.management',
#        'django.core.management.commands',
#        'django.core.management.commands.runserver',
#        'django.contrib.admin',
#        'django.contrib.auth',
#        'django.contrib.contenttypes',
#        'django.contrib.sessions',
#        'django.contrib.messages',
#        'django.contrib.staticfiles',
#        # Add any other Django apps or third-party packages you're using
#    ],
#    hookspath=[],
#    hooksconfig={},
#    runtime_hooks=[],
#    excludes=[],
#    win_no_prefer_redirects=False,
#    win_private_assemblies=False,
#    noarchive=False,
#)
#
#pyz = PYZ(a.pure, a.zipped_data)
#
#exe = EXE(
#    pyz,
#    a.scripts,
#    a.binaries,
#    a.zipfiles,
#    a.datas,
#    [],
#    name='SciDentAI-server',
#    debug=False,
#    bootloader_ignore_signals=False,
#    #strip=True,
#    upx=True,
#    upx_exclude=[],
#    runtime_tmpdir=None,
#    console=True,
#    disable_windowed_traceback=False,
#    argv_emulation=False,
#    target_arch=None,
#    codesign_identity=None,
#    entitlements_file=None,
#    icon=['../icons/SciDentAI_win-icon.ico'],
#    onefile=True,  # This option creates a single executable file
#)
# The COLLECT call is not needed for onefile mode, so it's removed
