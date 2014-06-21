
import os

def _find_exe_in_registry():
	from _winreg import OpenKey, QueryValue, HKEY_LOCAL_MACHINE
	import shlex
	keys = (
	   r"SOFTWARE\Classes\FirefoxHTML\shell\open\command",
	   r"SOFTWARE\Classes\Applications\firefox.exe\shell\open\command"
	)
	command = ""
	for path in keys:
		try:
			key = OpenKey(HKEY_LOCAL_MACHINE, path)
			command = QueryValue(key, "")
			break
		except OSError:
			pass
	else:
		return ""

	return shlex.split(command)[0]

def _default_windows_location():
	program_files = os.getenv("PROGRAMFILES", r"\Program Files")
	return os.path.join(program_files, "Mozilla Firefox\\firefox.exe")	
	
if __name__ == '__main__':
	print "firefox_exe_in_registry:  ", _find_exe_in_registry()
	print "default_windows_location: ", _default_windows_location()