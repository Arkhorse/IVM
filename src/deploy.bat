e:
cd "E:\Python/IVM\IVM\src\gui\mods"
python -m py_compile mod_ivm.py
move /y "E:\Python\IVM\IVM\src\gui\mods\mod_ivm.pyc" "E:\Python\IVM\IVM\src\ivm\res\scripts\client\gui\mods\"
cd "E:\Python\IVM\IVM\src\gui\IVM"
python -m py_compile __init__.py
python -m py_compile _config.py
python -m py_compile battle.py
python -m py_compile fixes.py
python -m py_compile hanger.py
python -m py_compile mod_constants.py
python -m py_compile sounds.py
cd ../../..
move /y "E:\Python\IVM\IVM\src\gui\mods\IVM\__init__.pyc" "E:\Python\IVM\IVM\src\ivm\res\scripts\client\gui\IVM\"
move /y "E:\Python\IVM\IVM\src\gui\mods\IVM\_config.pyc" "E:\Python\IVM\IVM\src\ivm\res\scripts\client\gui\IVM\"
move /y "E:\Python\IVM\IVM\src\gui\mods\IVM\battle.pyc" "E:\Python\IVM\IVM\src\ivm\res\scripts\client\gui\IVM\"
move /y "E:\Python\IVM\IVM\src\gui\mods\IVM\fixes.pyc" "E:\Python\IVM\IVM\src\ivm\res\scripts\client\gui\IVM\"
move /y "E:\Python\IVM\IVM\src\gui\mods\IVM\hanger.pyc" "E:\Python\IVM\IVM\src\ivm\res\scripts\client\gui\IVM\"
move /y "E:\Python\IVM\IVM\src\gui\mods\IVM\mod_constants.pyc" "E:\Python\IVM\IVM\src\ivm\res\scripts\client\gui\IVM\"
move /y "E:\Python\IVM\IVM\src\gui\mods\IVM\sounds.pyc" "E:\Python\IVM\IVM\src\ivm\res\scripts\client\gui\IVM\"
cd "E:\Python\IVM\IVM\src\ivm"
7z a -tzip -mx0 TheIllusion.IVM.wotmod "res"
move /y "E:\Python\IVM\IVM\src\IVM\TheIllusion.IVM.wotmod" "J:\World_of_Tanks_NA\mods\1.8.0.2\"
pause
