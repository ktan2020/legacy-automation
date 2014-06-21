from sst.actions import *

import sys
if sys.platform.startswith("linux"):
	from pyvirtualdisplay import Display
	display = Display(visible=0, size=(1024, 768))
else:
	display = None

if display != None:
	display.start()

go_to('http://finance.search.yahoo.com/')
assert_title_contains('Yahoo')
element = get_element(id='yschsp')
write_textfield(element, 'AMZN', clear=False)
click_button('yschbt')
assert_title_contains('AMZN - Yahoo')

if display != None:
	display.stop()
