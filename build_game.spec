# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['2048.py'],
             pathex=['D:\DevelopSoftware\Project\python\test\2048.py'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='2048',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)
datas = [('path_to_python_dll\python311.dll', '.'),]

