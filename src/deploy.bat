@echo off
e:
cd "E:\Python\IVM\IVM\src"
echo "Compiling"
@echo off
python -m py_compile mod_ivm.py
move /y "E:\Python\IVM\IVM\src\mod_ivm.pyc" "E:\Python\IVM\IVM\src\IVM\res\scripts\client\gui\mods\"
cd "E:\Python\IVM\IVM\src\IVM"
echo "Ziping and moving"
@echo off
7z a -tzip -mx0 TheIllusion.IVM.wotmod "res"
move /y "E:\Python\IVM\IVM\src\IVM\TheIllusion.IVM.wotmod" "J:\World_of_Tanks_NA\mods\1.9.0.0\"
echo "Finished"
pause