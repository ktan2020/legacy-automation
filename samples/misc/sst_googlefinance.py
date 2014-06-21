from sst.actions import *

import sys
if sys.platform.startswith("linux"):
	from pyvirtualdisplay import Display
	display = Display(visible=0, size=(1024, 768))
else:
	display = None

if display != None:
	display.start()

set_base_url('http://www.google.com/')

go_to('/')
assert_title_contains('Google')

go_to('/finance')
assert_url('/finance')
assert_title_contains('Google Finance: Stock market')

write_textfield(get_element(name='q'), 'IBM')
click_button('gbqfb')
assert_url_contains('IBM')
assert_title_contains('International Business Machines')

if display != None:
	display.stop()