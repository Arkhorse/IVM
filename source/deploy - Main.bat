cls
@echo off
e:
cd "E:\Python\IVM\IVM\source\ivm"
echo "Ziping and moving"
@echo off
7z a -tzip -mx0 com.ivm.wotmod "meta.xml" "LICENSE.txt" "res"
move /y "E:\Python\IVM\IVM\source\ivm\com.ivm.wotmod" "H:\World_of_Tanks_NA\mods\1.9.1.1\"
echo "Finished"
pause