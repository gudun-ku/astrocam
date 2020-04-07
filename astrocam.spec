# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['astrocam.py', 'constants.py', 'fileuploader.py', 'imagepacker.py'],
             pathex=['D:\\projects\\astrocam'],
             binaries=[],
             datas=[],
             hiddenimports=['os.path', 'os.path.abspath', 'patoolib', 'patoolib.programs', 'patoolib.programs.rar'],
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
          name='astrocam',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='astrocam')
import shutil
shutil.copyfile('areas.txt', '{0}/astrocam/areas.txt'.format(DISTPATH))