cls
@echo off

rem all my set variables. Makes my life easier.
rem this is for "public" release. Not a Relhax folder structure.
set "versiondir=1.10.0.1"
set "Dependencies=E:\Python\IVM\IVM\Dependencies"
set "publishDir=E:\Python\IVM\IVM\Publish"
rem possible states: Development, Beta, Released
set "ivmStatus=Development"
set "ivmVersion=0.06"

rem Remove old files

rd /q /s "%publishDir%\mods"
rd /q /s "%publishDir%\res_mods"

rem Make Dirs

md "mods/%versiondir%/"
md "mods/configs/"
md "res_mods/%versiondir%/"
md "res_mods/%versiondir%/audioww/"

echo "Copying Files"
@echo off
xcopy /v /y "%Dependencies%\izeberg.modsettingsapi_1.3.0.wotmod" "%publishDir%\mods\%versiondir%\"
xcopy /v /y "%Dependencies%\poliroid.modslistapi_1.3.3.wotmod" "%publishDir%\mods\%versiondir%\"

rem xCopy will make these folders. Found not already having the mods and res_mods folders made at the start causes issues
xcopy /v /y "%Dependencies%\PYmodsCore.wotmod" "%publishDir%\mods\%versiondir%\PYmods\"
rem xcopy /v /y "%Dependencies%\en.json" "%publishDir%\mods\configs\PYmods\PYmodsGUI\i18n\"
rem xcopy /v /y "%Dependencies%\de.json" "%publishDir%\mods\configs\PYmods\PYmodsGUI\i18n\"
rem xcopy /v /y "%Dependencies%\ru.json" "%publishDir%\mods\configs\PYmods\PYmodsGUI\i18n\"

rem This makes my wotmod, so I dont need to run yet another bat to do this. Deja Vue...
rem The compiling is done using a py, as the bat method isnt as short. Plus its part of my work space in VS, so I dont need to open it
e:
cd "E:\Python\IVM\IVM\source\ivm"
7z a -tzip -mx0 com.ivm.%ivmVersion%.wotmod "meta.xml" "LICENSE.txt" "res"

@echo off

xcopy /v /y "E:\Python\IVM\IVM\source\ivm\com.ivm.%ivmVersion%.wotmod" "%publishDir%\mods\%versiondir%\"
xcopy /v /y "E:\Python\IVM\IVM\source\engine_config.xml" "%publishDir%\res_mods\%versiondir%\"
xcopy /v /y "E:\Python\IVM\IVM\source\audio\IVM.bnk" "%publishDir%\res_mods\%versiondir%\audioww\"
xcopy /v /y "E:\Python\IVM\IVM\source\audio\audio_mods.xml" "%publishDir%\res_mods\%versiondir%\audioww\"

rem pause

cd %publishDir%

echo "Making Zip"
@echo off
7z a -tzip -mx0 IVM.%ivmStatus%.%ivmVersion%.%versiondir%.zip "mods" "res_mods" 
pause