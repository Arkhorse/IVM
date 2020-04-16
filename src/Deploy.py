import compileall
import shutil
import os

source_loader = 'E:\Python\IVM\IVM\src\gui\mods\mod_IVM.pyc'
destination_loader = 'E:/Python/IVM/IVM/src/ivm/res/scripts/client/gui/mods'
source = ['E:/Python/IVM/IVM/src/gui/mods/IVM/__init__.pyc', 'E:/Python/IVM/IVM/src/gui/mods/IVM/_config.pyc', 'E:/Python/IVM/IVM/src/gui/mods/IVM/battle.pyc', 'E:/Python/IVM/IVM/src/gui/mods/IVM/fixes.pyc', 'E:/Python/IVM/IVM/src/gui/mods/IVM/hanger.pyc', 'E:/Python/IVM/IVM/src/gui/mods/IVM/mod_constants.pyc', 'E:/Python/IVM/IVM/src/gui/mods/IVM/sounds.pyc']
destination = 'E:/Python/IVM/IVM/src/ivm/res/scripts/client/gui/IVM'

compileall.compile_dir('E:/Python/IVM/IVM/src/gui', force=False)

if not os.path.exists(destination):
    os.makedirs(destination)
if not os.path.exists(destination_loader):
    os.makedirs(destination_loader)
for files in source:
    if files.endswith('.pyc'):
        shutil.move(files,destination)

print 'All Done'