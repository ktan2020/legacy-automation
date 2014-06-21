/*
	Sample from learnsoapui.wordpress.com
 */

@Grapes([
	@Grab("commons-io:commons-io"),
	@Grab("org.seleniumhq.selenium:selenium-firefox-driver"),
	@Grab("org.seleniumhq.selenium:selenium-support")])
	
import org.openqa.selenium.By
import org.openqa.selenium.WebDriver
import org.openqa.selenium.WebElement
import org.openqa.selenium.firefox.FirefoxDriver
import org.openqa.selenium.support.ui.ExpectedCondition
import org.openqa.selenium.support.ui.WebDriverWait
import org.openqa.selenium.OutputType
import org.apache.commons.io.FileUtils
import org.openqa.selenium.Keys
 
 
WebDriver driver = new FirefoxDriver()   
 
try
{
	driver.get("https://learnsoapui.wordpress.com") // Url to be opened
	println driver.getSessionId().toString()
 
	WebElement element = driver.findElement(By.id("s"))
	assert element != null
	element.sendKeys("Assertion")
 	element.submit()
 
	//new BufferedReader(new InputStreamReader(System.in)).readLine()
 
	driver.getKeyboard().pressKey(Keys.DOWN)
	driver.getKeyboard().pressKey(Keys.DOWN)
	driver.getKeyboard().pressKey(Keys.DOWN)
	driver.getKeyboard().pressKey(Keys.UP)
	driver.getKeyboard().pressKey(Keys.UP)
	driver.getKeyboard().pressKey(Keys.UP)
} catch(Exception e) {
	println "Exception encountered : " + e.message
} finally {
	File f1 = driver.getScreenshotAs(OutputType.FILE)
	FileUtils.copyFile(f1, new File("screenshot.png"));
}

driver.quit()

println "Done!"