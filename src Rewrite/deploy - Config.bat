@echo off
e:
cd "E:\Python\IVM\IVM\src Rewrite"
echo "Compiling"
@echo off
python -m py_compile config.py
move /y "E:\Python\IVM\IVM\src Rewrite\config.pyc" "E:\Python\IVM\IVM\src Rewrite\core\res\scripts\client\gui\mods\"
echo Config Done
exit