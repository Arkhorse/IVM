@echo off
e:
cd "E:\Python\IVM\IVM\src Rewrite"
echo "Compiling"
@echo off
python -m py_compile mod_ivm.py
move /y "E:\Python\IVM\IVM\src Rewrite\mod_ivm.pyc" "E:\Python\IVM\IVM\src Rewrite\ivm\res\scripts\client\gui\mods\"
cd "E:\Python\IVM\IVM\src Rewrite\ivm"
echo "Ziping and moving"
@echo off
7z a -tzip -mx0 IVM.Main.wotmod "res"
move /y "E:\Python\IVM\IVM\src Rewrite\ivm\IVM.Main.wotmod" "J:\World_of_Tanks_NA\mods\1.9.0.2\"
echo "Finished"
pause