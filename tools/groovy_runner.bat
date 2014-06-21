@echo off
setlocal EnableDelayedExpansion

echo. *** [JAVA_HOME = %JAVA_HOME%] [JDK_HOME = %JDK_HOME%] ***

set CLASSPATH="
for /F "delims=" %%a in ('dir /b /s %TOOLCHAIN%\libs\java\*.jar %TOOLCHAIN%\libs\webdriver\*.jar') do (
set CLASSPATH=!CLASSPATH!;%%a
)
set CLASSPATH=!CLASSPATH!;"

echo. *** [CLASSPATH] : !CLASSPATH! ***

cmd /c groovy -cp %CLASSPATH% %*
set ERRORSTATUS=%ERRORLEVEL%

echo. @@@ groovy return code: [%ERRORSTATUS%] @@@  

:end
endlocal & exit /B %ERRORSTATUS%