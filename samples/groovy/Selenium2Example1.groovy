
@Grapes([
	@Grab("commons-lang:commons-lang"),
	@Grab("commons-io:commons-io"),
	@Grab("org.seleniumhq.selenium:selenium-firefox-driver"),
	@Grab("org.seleniumhq.selenium:selenium-support")])

	
import java.util.concurrent.TimeUnit
import org.apache.commons.lang.RandomStringUtils
import org.apache.commons.io.FileUtils
import org.openqa.selenium.By
import org.openqa.selenium.OutputType
import org.openqa.selenium.WebDriver
import org.openqa.selenium.firefox.FirefoxDriver
import org.openqa.selenium.TakesScreenshot


def driver = new FirefoxDriver()
driver.manage().timeouts().implicitlyWait(20, TimeUnit.SECONDS)

// generate some random junk string and use that as search term
def randomJunk = RandomStringUtils.randomAlphanumeric(20)

driver.get("http://duckduckgo.com/")

def txtSearch = driver.findElement(By.name("q"))
txtSearch.sendKeys(randomJunk)
def btnSubmit = driver.findElement(By.xpath("//input[@type='submit']"))
btnSubmit.click()

def txtResults = driver.findElement(By.id("links_wrapper"))
while (!txtResults.isDisplayed())
	Thread.sleep(100)
txtSearch = driver.findElement(By.name("q"))

// "out of the box" asserts are much more primitive
assert txtResults.getText() != null

assert driver.getCurrentUrl().contains("?q=")
assert driver.getCurrentUrl().endsWith(randomJunk)

File scrFile = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
FileUtils.copyFile(scrFile, new File("screenshot.png"));

// dismiss the browser - no tearDown() here
driver.quit()

println("If you can see this, the test succeeded!")