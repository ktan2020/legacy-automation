from sst.actions import *

import sys
if sys.platform.startswith("linux"):
	from pyvirtualdisplay import Display
	display = Display(visible=0, size=(1024, 768))
else:
	display = None

if display != None:
	display.start()
	
go_to('http://seleniumhq.org/')
assert_title('Selenium - Web Browser Automation')

if display != None:
	display.stop()