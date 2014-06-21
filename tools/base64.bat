@setlocal enabledelayedexpansion && python -x "%~f0" %* & exit /b !ERRORLEVEL!
import base64, sys
from optparse import OptionParser
p = OptionParser()
p.add_option("-d", "--decode", action="store_true", dest="decode", help="Decode data")
(opts, args) = p.parse_args()
if len(args)==0: exit()
str = open(args[0]).read()
if opts.decode:
	print base64.standard_b64decode(str)
else:
	print base64.standard_b64encode(str)