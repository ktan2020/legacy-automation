@echo off
setlocal EnableDelayedExpansion

:GETOPTS
if /I "%1" == "" goto Help
if /I %1 == -h goto Help
if /I %1 == --help goto Help
if /I %1 == --env set ENV=%2 & shift
shift
if not (%1)==() (
	set SCRIPT_NAME=%1
	goto GETOPTS
)

goto start
:Help
echo.Usage: %~n0 [--env Environment to use]
echo. 
goto end
:start
if "%ENV%" == "" goto Help

set ENV=%ENV: =%
set RUNNER_OUT=_output_.txt

echo. *** [ENV = %ENV%]
echo. *** [JAVA_HOME = %JAVA_HOME%] [JDK_HOME = %JDK_HOME%] ***

set CLASSPATH="
for /F "delims=" %%a in ('dir /b /s %TOOLCHAIN%\libs\java\ %TOOLCHAIN%\libs\junit-4.11.jar %TOOLCHAIN%\libs\ojdbc5.jar jars\*.jar') do (
	set CLASSPATH=!CLASSPATH!;%%a
)
set CLASSPATH=!CLASSPATH!;"

echo. *** [CLASSPATH] : !CLASSPATH! ***

cmd /c groovy -cp %CLASSPATH% %SCRIPT_NAME% | tee %RUNNER_OUT% 
rem cmd /c groovy %*
set ERRORSTATUS=%ERRORLEVEL%

echo. @@@ groovy return code: [%ERRORSTATUS%] @@@  

if not exist %RUNNER_OUT% (
	echo "XXX FATAL: (%RUNNER_OUT%) not present - tee output missing. XXX"
	goto end
)

:: errors / failures both set error status to 1

set RE='.*Failures: *(\d+)'
for /F "delims=" %%i in ('grep "Failures:" %RUNNER_OUT% ^| tail -1 ^| python -c "import re,sys;m=re.compile(%RE%).match(sys.stdin.read());print m.groups()[0] if m else 0"') do set RUNNERFAILURES=%%i
if not "%RUNNERFAILURES%" == "0" (
	echo Found failures: %RUNNERFAILURES%
	set ERRORSTATUS=1
)
set RE='.*Errors: *(\d+)'
for /F "delims=" %%i in ('grep "Errors:" %RUNNER_OUT% ^| tail -1 ^| python -c "import re,sys;m=re.compile(%RE%).match(sys.stdin.read());print m.groups()[0] if m else 0"') do set RUNNERERRORS=%%i
if not "%RUNNERERRORS%" == "0" (
	echo Found errors: %RUNNERERRORS%
	set ERRORSTATUS=1
)

echo. ### runner return code: [%ERRORSTATUS%] ###

:end
rem del /F /Q %RUNNER_OUT% 2>NUL
endlocal & exit /B %ERRORSTATUS%
