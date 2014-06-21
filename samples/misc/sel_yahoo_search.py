import sys
if sys.platform.startswith("linux"):
	from pyvirtualdisplay import Display
	display = Display(visible=0, size=(1024, 768))
else:
	display = None

if display != None:
	display.start()

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox() # Get local session of firefox
browser.get("http://www.yahoo.com") # Load page
assert "Yahoo" in browser.title
elem = browser.find_element_by_name("p") # Find the query box
elem.send_keys("seleniumhq" + Keys.RETURN)
time.sleep(1.5) # Let the page load - XXX An example of what NOT to do XXX

try:
	browser.find_element_by_link_text("Selenium - Web Browser Automation")
except NoSuchElementException:
    browser.save_screenshot("test-selenium-failed.jpg")
    assert 0, "can't find seleniumhq"

browser.close()

if display != None: 
	display.stop()