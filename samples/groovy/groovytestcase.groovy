import java.util.concurrent.TimeUnit
import groovyx.net.http.URIBuilder
import org.apache.commons.lang.RandomStringUtils
import org.openqa.selenium.By
import org.openqa.selenium.WebDriver
import org.openqa.selenium.firefox.FirefoxDriver

@Grapes([
	@Grab("org.gebish:geb-core:0.9.2"),
	@Grab("org.seleniumhq.selenium:selenium-firefox-driver"),
	@Grab("org.seleniumhq.selenium:selenium-support"),
	@Grab("commons-lang:commons-lang:2.6"),
	@Grab("org.codehaus.groovy.modules.http-builder:http-builder" )
	])
class MyTest extends GroovyTestCase {

	def driver;
	
	void setUp() { 
		driver = new FirefoxDriver(); 
		driver.manage().timeouts().implicitlyWait(20, TimeUnit.SECONDS) 
	}
	
	void tearDown() {
		driver.quit()
	}
	
	void test1() {
		def randomJunk = RandomStringUtils.randomAlphanumeric(20)

		driver.get("http://duckduckgo.com/")

		def txtSearch = driver.findElement(By.name("q"))
		txtSearch.sendKeys(randomJunk)
		
		def btnSubmit = driver.findElement(By.xpath("//input[@type='submit']"))
		btnSubmit.click()

		// This will trigger a failure !!!
		def txtResults = driver.findElement(By.id("nrreld"))
		while (!txtResults.isDisplayed())
			Thread.sleep(100)
		txtSearch = driver.findElement(By.name("q"))

		// "out of the box" asserts are much more primitive
		assert txtResults.getText().contains("No results.")
		assert txtSearch.getAttribute("value").equals(randomJunk)

		def currentURL = new URIBuilder(driver.getCurrentUrl())
		assert currentURL.query.containsKey("q")
		assert currentURL.query.q.equals(randomJunk)

		println("If you can see this, the test succeeded!")
	}
	
}