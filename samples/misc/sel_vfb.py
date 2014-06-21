#!/usr/bin/env python

import sys
from selenium import webdriver

if sys.platform.startswith("linux"):
	from pyvirtualdisplay import Display
	display = Display(visible=0, size=(1024, 768))
else:
	display = None

if display != None:
	display.start()

# now Firefox will run in a virtual display. 
# you will not see the browser.
browser = webdriver.Firefox()
browser.get('http://www.google.com')
print browser.title
browser.get_screenshot_as_file('screenshot.png')
browser.quit()

if display != None:
	display.stop()
