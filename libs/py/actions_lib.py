
import params
import unittest, time, datetime, os, sys
import sst.actions
#from robot.api import logger


# XXX FIXME XXX
__TESTCASE_ID__ = None

class ActionsLibBaseTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		sst.actions.start()
		
	@classmethod
	def tearDownClass(cls):
		sst.actions.stop()
		
	def setUp(self):
		global __TESTCASE_ID__
		__TESTCASE_ID__ = self.id()
		
	def tearDown(self):
		pass


class FailedSeleniumAssertion(object):
	def __init__(self, error, screenshot, pagedump):
		self.error = error
		self.screenshot = screenshot
		self.pagedump = pagedump
		
	def __call__(self, f):
		def wrappedfunction(*args, **kwargs):
			try:
				return f(*args, **kwargs)
			except self.error:	
				sst.actions._print("Caught an AssertionError: <<< " + str(sys.exc_info()[1]) + " >>>")
				if self.screenshot is not None: self.screenshot()
				if self.pagedump is not None: self.pagedump() 
				raise
		return wrappedfunction	

		
sst.config.results_directory = os.getenv('SCREENSHOT_DIR','screenshots')
sst.actions._make_results_dir()
params.SCREENSHOT_DIR = sst.config.results_directory


def take_screenshot(name=None):
	global __TESTCASE_ID__
	
	if name==None:
		filename = '%s.png' % __TESTCASE_ID__
	else:
		filename = '%s.png' % (str(name)+'-'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
	sst.actions.take_screenshot(filename)
	with open(os.path.join(params.SCREENSHOT_DIR,filename),'rb') as f:
		import base64
		#logger.info('<img src="data:image/png;base64,%s" width="1200px"/>' % (base64.b64encode(f.read())), True, False)
    
	
def dump_pagesource(name=None):
	global __TESTCASE_ID__
	
	sst.actions._print('Capturing page source')
	if name==None:
		filename = '%s.html' % __TESTCASE_ID__
	else:
		filename = '%s.html' % name

	path = os.path.join(sst.config.results_directory, filename)
	import codecs
	with codecs.open(path, 'w', encoding='utf-8') as f:
		f.write(sst.actions.get_page_source())


def start():
    sst.actions.start()
    
def stop():
    sst.actions.stop()
    
def go_to(url):
    sst.actions.go_to(url)    

def go_back():
    sst.actions.go_back()
    
def set_base_url(url):
	sst.actions.set_base_url(url)

def get_base_url(url):
	return sst.actions.get_base_url(url)
	
def get_page_source():
    return sst.actions.get_page_source()

def sleep(secs):
    sst.actions.sleep(secs)

def refresh():
    sst.actions.refresh()

def maximize_window():
	get_selenium_driver_object().maximize_window()	

def close_window():
	sst.actions.close_window()
	
def clear_cookies():
	sst.actions.clear_cookies()
	
def get_cookies():
	return sst.actions.get_cookies()
	
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def get_element(tag=None, css_class=None, id=None, text=None, text_regex=None, **kwargs):
	return sst.actions.get_element(tag=tag, css_class=css_class, id=id, text=text, text_regex=text_regex, **kwargs)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def get_elements(tag=None, css_class=None, id=None, text=None, text_regex=None, **kwargs):
	return sst.actions.get_elements(tag=tag, css_class=css_class, id=id, text=text, text_regex=text_regex, **kwargs)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def get_elements_by_css(selector):
	return sst.actions.get_elements_by_css(selector)
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def get_element_by_css(selector):	
	return sst.actions.get_element_by_css(selector)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def get_element_by_xpath(selector):
	return sst.actions.get_element_by_xpath(selector)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def get_elements_by_xpath(selector):
	return sst.actions.get_elements_by_xpath(selector)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def exists_element(tag=None, css_class=None, id=None, text=None, text_regex=None, **kwargs):
	return sst.actions.exists_element(tag=tag, css_class=css_class, id=id, text=text, text_regex=text_regex, **kwargs)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def click_link(id_or_elem):
	sst.actions.click_link(id_or_elem)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def click_element(id_or_elem):
	sst.actions.click_element(id_or_elem)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def click_button(id_or_elem):
	sst.actions.click_button(id_or_elem)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def write_textfield(id_or_elem, text):
	sst.actions.write_textfield(id_or_elem, text)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def toggle_checkbox(id_or_elem):
	sst.actions.toggle_checkbox(id_or_elem)
	
def set_wait_timeout(timeout):
	sst.actions.set_wait_timeout(timeout)
	
def wait_for(condition, *args, **kwargs):
	sst.actions.wait_for(condition, *args, **kwargs)
	
def wait_for_and_refresh(condition):
	sst.actions.wait_for_and_refresh(condition)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def set_dropdown_value(id_or_elem, text=None, value=None):
	sst.actions.set_dropdown_value(id_or_elem, text, value)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def set_radio_value(id_or_elem):
	sst.actions.set_radio_value(id_or_elem)
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def get_text(elem):
	sst.actions._get_text(elem)
	
def get_selenium_driver_object():
	return sst.actions.browser
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def assert_fail(msg):
    assert False, msg

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def assert_dropdown(id_or_elem):
	sst.actions.assert_dropdown(id_or_elem)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def assert_dropdown_value(id_or_elem, text_in):
	sst.actions.assert_dropdown_value(id_or_elem, text_in)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def assert_radio(id_or_elem):
	sst.actions.assert_radio(id_or_elem)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def assert_radio_value(id_or_elem, value):
	sst.actions.assert_radio_value(id_or_elem, value)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def assert_element(tag=None, css_class=None, id=None, text=None, text_regex=None, **kwargs):
	sst.actions.assert_element(tag=tag, css_class=css_class, id=id, text=text, text_regex=text_regex, **kwargs)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def assert_button(id_or_elem):
	sst.actions.assert_button(id_or_elem)
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def assert_textfield(id_or_elem):
	assert sst.actions.assert_textfield(id_or_elem) is not None

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def assert_checkbox(id_or_elem):
	assert sst.actions.assert_checkbox(id_or_elem) is not None
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def assert_link(id_or_elem):
	assert sst.actions.assert_link(id_or_elem) is not None

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def assert_element_exist(id):
	assert sst.actions.exists_element(id=id), "Element %s doesn't exist" % id

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def assert_element(tag=None, css_class=None, id=None, text=None, text_regex=None, **kwargs):
	assert sst.actions.assert_element(tag=tag, css_class=css_class, id=id, text=text, text_regex=text_regex, **kwargs) is not None
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def assert_attribute(id_or_elem, attribute, value, regex=True):
	sst.actions.assert_attribute(id_or_elem, attribute, value, regex)
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def assert_css_property(id_or_elem, property, value, regex=True):
	sst.actions.assert_css_property(id_or_elem, property, value, regex)	
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def assert_displayed(id_or_elem):
	assert sst.actions.assert_displayed(id_or_elem) is not None
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def assert_page_contains(text):
	_assert_in_page(text)
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def assert_page_does_not_contain(text):
	_assert_not_in_page(text)
			
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)				
def assert_title(title):
	sst.actions.assert_title(title)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)		
def assert_title_contains(text, regex=True):
	sst.actions.assert_title_contains(text, regex)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)		
def assert_url(url):
	sst.actions.assert_url(url)
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)		
def assert_url_contains(text, regex=True):
	sst.actions.assert_url_contains(text, regex)
    
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)		
def assert_table_has_rows(id_or_elem, num_rows):
	sst.actions.assert_table_has_rows(id_or_elem, num_rows)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def assert_table_row_contains_text(id_or_elem, row, contents, regex=True):
	sst.actions.assert_table_row_contains_text(id_or_elem, row, contents, regex)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def assert_text(id_or_elem, text):
	sst.actions.assert_text(id_or_elem, text)

@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)
def assert_text_contains(id_or_elem, text, regex=True):
	sst.actions.assert_text_contains(id_or_elem, text, regex)

def _assert_in_page(item, msg = "assertion failed: expected %(item)r in %(sequence)r"):
    """Assert that the item is in the sequence."""
    sequence = sst.actions.get_page_source()
    assert item in sequence, msg % {'item':item, 'sequence':sequence}

def _assert_not_in_page(item, msg="assertion failed: expected %(item)r not in %(sequence)r"):
    """Assert that the item is not in the sequence."""
    sequence = sst.actions.get_page_source()
    assert item not in sequence, msg % {'item':item, 'sequence':sequence}
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def assert_equal(first, second):
    """Assert two objects are equal."""
    sst.actions.assert_equal(first, second)
	
#assert_equals = assert_equal	
	
@FailedSeleniumAssertion(error=AssertionError, screenshot=take_screenshot, pagedump=dump_pagesource)	
def assert_not_equal(first, second):
    """Assert two objects are not equal."""
    sst.actions.assert_not_equal(first, second)
	
#assert_not_equals = assert_not_equal	

'''	
def set_bpx():
	import pdb; pdb.set_trace()
'''