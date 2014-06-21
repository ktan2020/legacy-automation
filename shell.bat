@echo off
rem setlocal

rem =================================================================
rem TODO: 
rem     * setup virtualenv workspace directory as user sandbox ...    
rem  
rem =================================================================

set drive=%~dp0
set drivep=%drive%
if #%drive:~-1%# == #\# set drivep=%drive:~0,-1%

set TOOLCHAIN=%drivep%
set PATH=%drivep%\win;%drivep%\tools;%drivep%\win\Scripts;%PATH%
set WEBDRIVER_PATH=%TOOLCHAIN%\libs\webdriver
set PATH=%PATH%;%WEBDRIVER_PATH%
set PYTHONPATH=%drivep%\libs\py
set PYTHONEXE=%drivep%\win\python.exe

set TERM=dumb
rem avoid collisions with other perl stuff on your system
set PERL_JSON_BACKEND=
set PERL_YAML_BACKEND=
set PERL5LIB=
set PERL5OPT=
set PERL_MM_OPT=
set PERL_MB_OPT=

echo.
echo. ----------------------------------------------
echo.           Automation ToolKit
echo.
type logo.txt
echo.
type readme.txt
echo.
echo. ----------------------------------------------
echo.

rem Sanitize windows path for sed to consume
for /F "delims=" %%a in ('echo %PYTHONEXE% ^| sed "s|\\|\\\\|g"') do @set PYTHONEXE=%%a
rem echo %PYTHONEXE%

title Automation Console

rem if exist sandbox\NUL GOTO END 
rem python win\python\Scripts\virtualenv.py sandbox
rem
:END
rem set PATH=%PATH%;%drivep%\sandbox\Scripts
rem cmd /k activate sandbox

echo.
echo.

rem endlocal
cmd /k