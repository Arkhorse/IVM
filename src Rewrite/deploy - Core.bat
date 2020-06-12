@echo off
e:
cd "E:\Python\IVM\IVM\src Rewrite"
echo "Compiling"
@echo off
python -m py_compile settings.py
move /y "E:\Python\IVM\IVM\src Rewrite\settings.pyc" "E:\Python\IVM\IVM\src Rewrite\core\res\scripts\client\gui\mods\"
cd "E:\Python\IVM\IVM\src Rewrite"
start "deploy - Config.bat"
pause
start "deploy - Template.bat"
pause
cd "E:\Python\IVM\IVM\src Rewrite\core"
echo "Ziping and moving"
@echo off
7z a -tzip -mx0 IVM.Core.wotmod "res"
move /y "E:\Python\IVM\IVM\src Rewrite\core\IVM.Core.wotmod" "J:\World_of_Tanks_NA\mods\1.9.0.1\"
echo "Finished"
pause