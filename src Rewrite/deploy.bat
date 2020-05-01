@echo off
e:
cd "E:\Python\IVM\IVM\src Rewrite"
echo "Compiling"
@echo off
python -m py_compile mod_ivm.py
move /y "E:\Python\IVM\IVM\src Rewrite\mod_ivm.pyc" "E:\Python\IVM\IVM\src Rewrite\IVM\res\scripts\client\gui\mods\"
cd "E:\Python\IVM\IVM\src Rewrite\IVM"
echo "Ziping and moving"
@echo off
7z a -tzip -mx0 TheIllusion.IVM.wotmod "res"
move /y "E:\Python\IVM\IVM\src Rewrite\IVM\TheIllusion.IVM.wotmod" "J:\World_of_Tanks_NA\mods\1.9.0.1\"
echo "Finished"
