
import time
import BaseHTTPServer
import sys
#import lxml.etree as ET
import xml.etree.ElementTree as ET


HOST_NAME = 'localhost' 
PORT_NUMBER = 9000 

REPLY = '''
<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
'''
REPLY = ''.join(REPLY.splitlines())
#ET.tostring(ET.fromstring(''.join(REPLY.splitlines())))


nodes = ET.fromstring(REPLY).findall("country")
for n in nodes:	
	print n.attrib['name']
print [ n.attrib['name'] for n in nodes ]


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
			
	def do_GET(s):
		"""Respond to a GET request."""
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write("<html><head><title>GET</title></head>")
		s.wfile.write("<p>GET: PATH = %s</p>" % s.path)
		s.wfile.write("<p>Request: </p>")
		
		s.wfile.write("<body>")
		s.wfile.write("<form id='f' action='.' method='POST'>")
		s.wfile.write('<div><textarea rows="20" cols="80" name="req" form="f">blah blah blah ... yada yada yada ...</textarea></div>')
		s.wfile.write("<div><input type='submit' /></div>")
		s.wfile.write("</form>")
		s.wfile.write("</body>")
		s.wfile.write("</html>")
		s.wfile.flush()
		s.wfile.close()
		
	def do_POST(s):
		"""Respond to a POST request."""
		import cgi
		form = cgi.FieldStorage(
			fp=s.rfile,
			headers=s.headers,
			environ={"REQUEST_METHOD": "POST"}
		)
		#print s.headers
		for item in form.list:
			print "[%s = %s]" % (item.name, item.value)
			
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write("<html><head><title>POST</title></head>")
		s.wfile.write("<p>POST: PATH = %s</p>" % s.path)
		s.wfile.write("<p>Response: </p>")
		
		s.wfile.write("<body>")
		s.wfile.write('<div><textarea rows="20" cols="80" name="rep">')
		
		# write canned reply back ...
		s.wfile.write(REPLY)
		
		s.wfile.write("</textarea></div>")
		
		s.wfile.write("</body>")
		s.wfile.write("</html>")
		s.wfile.flush()
		s.wfile.close()

		
if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
		
	httpd.server_close()
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)