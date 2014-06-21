import org.ccil.cowan.tagsoup.Parser;
     
String ENCODING = "UTF-8"
 
@Grapes( @Grab('org.ccil.cowan.tagsoup:tagsoup:1.2') )      
def PARSER = new XmlSlurper(new Parser() )
 
def url = "http://www.bing.com/search?q=web+scraping"
 
new URL(url).withReader (ENCODING) { reader ->
 
    def document = PARSER.parse(reader)
    // Extracting information
	
	//JQuery selector: $('#results h3 a')
	//Example 1
	document.'**'.find{ it['@id'] == 'results'}.ul.li.div.div.h3.a.each { println it.text() }
	//Example 2
	document.'**'.find{ it['@id'] == 'results'}.'**'.findAll{ it.name() == 'h3'}.a.each { println it.text() }
	
}