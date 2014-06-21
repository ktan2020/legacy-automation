@setlocal enabledelayedexpansion && python -x "%~f0" %* & exit /b !ERRORLEVEL!
import sys, subprocess

s = set([])
for arg in sys.argv[1:]:	
	s = s.union(set(subprocess.check_output("search_by_tag %s"%arg, shell=True).split()))
	
print '\n'.join(sorted(list(s)))
