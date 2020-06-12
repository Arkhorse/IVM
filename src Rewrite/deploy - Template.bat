@echo off
e:
cd "E:\Python\IVM\IVM\src Rewrite"
echo "Compiling"
@echo off
python -m py_compile template.py
move /y "E:\Python\IVM\IVM\src Rewrite\template.pyc" "E:\Python\IVM\IVM\src Rewrite\core\res\scripts\client\gui\mods\"
echo Template Done
exit