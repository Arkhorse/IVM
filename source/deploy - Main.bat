cls
@echo off
rem Set Variables
set "versiondir=1.10.0.0"
set "Dependencies=E:\Python\IVM\IVM\Dependencies"
set "gameDir=I:\World_of_Tanks_NA\"

rem Set Drive Letter
e:

cd "E:\Python\IVM\IVM\source\ivm"
echo "Ziping and moving"
@echo off
7z a -tzip -mx0 com.ivm.wotmod "meta.xml" "LICENSE.txt" "res"
xcopy /v /y "E:\Python\IVM\IVM\source\ivm\com.ivm.wotmod" "%gameDir%\mods\%versiondir%\"
xcopy /v /y "E:\Python\IVM\IVM\source\engine_config.xml" "%gameDir%\res_mods\%versiondir%\"

xcopy /v /y "E:\Python\IVM\IVM\source\audio\IVM.bnk" "%gameDir%\res_mods\%versiondir%\audioww\"
xcopy /v /y "E:\Python\IVM\IVM\source\audio\audio_mods.xml" "%gameDir%\res_mods\%versiondir%\audioww\"

xcopy /v /y "E:\Python\IVM\IVM\Publish\mods\1.9.1.2\izeberg.modsettingsapi_1.3.0.wotmod" "%gameDir%\mods\%versiondir%\"
xcopy /v /y "E:\Python\IVM\IVM\Publish\mods\1.9.1.2\poliroid.modslistapi_1.3.2.wotmod" "%gameDir%\mods\%versiondir%\"

rem xCopy will make these folders. Found not already having the mods and res_mods folders made at the start causes issues
xcopy /v /y "E:\Python\IVM\IVM\Publish\mods\1.9.1.2\PYmods\PYmodsCore.wotmod" "%gameDir%\mods\%versiondir%\PYmods\"
xcopy /v /y "E:\Python\IVM\IVM\Publish\mods\configs\PYmods\PYmodsGUI\i18n\en.json" "%gameDir%\mods\configs\PYmods\PYmodsGUI\i18n\"
xcopy /v /y "E:\Python\IVM\IVM\Publish\mods\configs\PYmods\PYmodsGUI\i18n\de.json" "%gameDir%\mods\configs\PYmods\PYmodsGUI\i18n\"
xcopy /v /y "E:\Python\IVM\IVM\Publish\mods\configs\PYmods\PYmodsGUI\i18n\ru.json" "%gameDir%\mods\configs\PYmods\PYmodsGUI\i18n\"

echo "Finished"
pause