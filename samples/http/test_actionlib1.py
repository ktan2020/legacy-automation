from actions_lib import *

class MySimpleTest1(ActionsLibBaseTest):
	def test_google(self):
		set_base_url('http://www.google.com/')
		go_to('/')
		
		assert_title_contains('Google')
		assert_page_contains("Google Search")
		assert_page_does_not_contain("Apple Computer")

		go_to('/finance')
		assert_url('/finance')
		assert_title_contains('Google Finance: Stock market')

		write_textfield(get_element(name='q'), 'IBM')
		click_button('gbqfb')
		assert_url_contains('IBM')
		assert_title_contains('International Business Machines')
        
		take_screenshot()
		dump_pagesource()
		
	def test_yahoo(self):	
		go_to("http://www.yahoo.com")
		assert_title_contains("Yahoo")
		assert_page_contains("About Yahoo")
   
		# should redirect to finance.yahoo.com
		go_to('http://www.yahoo.com/finance')
		assert_url("http://finance.yahoo.com")
		assert_title_contains("Yahoo Finance")
		
		write_textfield(get_element(id='txtQuotes'), "IBM")
		click_button('btnQuotes')
		assert_url_contains("IBM")
		assert_title_contains('International Business Machines') 	
