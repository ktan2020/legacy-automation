@echo off
setlocal

SET SELENIUM_SERVER_JAR=%TOOLCHAIN%\libs\wd\selenium-server-standalone.jar
SET ROBOT_SYSLOG_LEVEL=INFO
SET ROBOT_SYSLOG_FILE=robot_syslog.txt
set ROBOT_REPORTDIR=robot_reports
set ROBOT_DEBUGFILE=robot_debug.txt
set NO_SOAPUI_REPORT=1

if defined DEBUG (
	winpdb %TOOLCHAIN%\tools\autorunner.py %*
	goto:cleanup
)

if not defined PROFILE (
	python %TOOLCHAIN%\tools\autorunner.py %*
) else ( 
	python -m cProfile -o profile.trace %TOOLCHAIN%\tools\autorunner.py %*
)

:cleanup runner droppings
rm -rf __pycache__ *.pyc 2>NUL
endlocal