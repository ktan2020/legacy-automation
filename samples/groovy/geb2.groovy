
@Grapes([
    @Grab("org.seleniumhq.selenium:selenium-firefox-driver"),
    @Grab("org.seleniumhq.selenium:selenium-support")
])

import org.openqa.selenium.By
import org.openqa.selenium.WebDriver
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.*


driver = new FirefoxDriver();

driver.get("http://google.com/ncr")
assert driver.getTitle() == "Google"

elem = driver.findElement(By.name("q"))

elem.sendKeys("wikipedia")
elem.submit()

(new WebDriverWait(driver, 10)).until(new ExpectedCondition<Boolean>() {
	public Boolean apply(WebDriver d) {
		return d.getTitle().endsWith("Google Search");
	}
});

// No-no !
Thread.sleep(2000)

elem = driver.findElements(By.cssSelector("li.g")).get(0)
assert elem != null

elem = elem.findElement(By.cssSelector("a.l"))
assert elem != null
assert elem.getText() == "Wikipedia"

elem.click()

(new WebDriverWait(driver, 10)).until(new ExpectedCondition<Boolean>() {
	public Boolean apply(WebDriver d) {
		return d.getTitle().contains("Wikipedia");
	}
});

driver.quit()

System.out.println("Done!")

