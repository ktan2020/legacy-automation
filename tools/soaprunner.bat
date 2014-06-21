@echo off
setlocal EnableDelayedExpansion

echo. *** soaprunner.bat called with params: [ %* ] ***

set SOAPUI_HOME=%TOOLCHAIN%\libs\soapui\bin
set CLASSPATH=%SOAPUI_HOME%\soapui.jar;%SOAPUI_HOME%\..\lib\*;
set JAVA_OPTS=-Xms128m -Xmx512m -Dsoapui.logroot="%SOAPUI_LOGSDIR%\\" -Dsoapui.properties=soapui.properties -Dsoapui.home="%SOAPUI_HOME%" -Dsoapui.ext.libraries="%SOAPUI_HOME%\ext"
set JAVA=java 
set SOAPUI_ERRORS_LOG=soapui-errors.log
set ERRORSTATUS=

if not exist "%SOAPUI_SETTINGS%" (call soapsettings)

:: handle multiple project files, error and exception handling ... 
for %%F in (%*) do (
	echo.  @@@ Running SoapUITestCaseRunner with param [%%F] @@@
	echo.  %JAVA% %JAVA_OPTS% com.eviware.soapui.tools.SoapUITestCaseRunner -r -a -j -M -f %SOAPUI_LOGSDIR% %DB_PROPERTIES% -t soapui-settings.xml %%F
	%JAVA% %JAVA_OPTS% com.eviware.soapui.tools.SoapUITestCaseRunner -r -a -j -M -f %SOAPUI_LOGSDIR% %DB_PROPERTIES% -t soapui-settings.xml %%F
	if errorlevel 1 (
		echo.  ERROR: [%%F] SoapUITestCaseRunner returned errorlevel [1]
		set ERRORSTATUS=1
	)

	for /F "delims=" %%A in ('wc -l %SOAPUI_LOGSDIR%\%SOAPUI_ERRORS_LOG% 2^>NUL ^| awk "{print $1}"') do (
		if "%%A" NEQ "0" (
			set ERRORSTATUS=1
			echo.  ERROR: [%%F] tripped SoapUITestCaseRunner - stack trace in [%SOAPUI_ERRORS_LOG%] 
		)
	)
)
:: end of for

if defined ERRORSTATUS (goto:error) else (goto:end)

:error
echo.  XXX ERROR: SoapUITestCaseRunner returned an error status. XXX

:end

rm -f soapui-settings.xml
endlocal & exit /B %ERRORSTATUS%