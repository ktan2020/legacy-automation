
@Grapes([
    @Grab("org.gebish:geb-core:0.9.2"),
    @Grab("org.seleniumhq.selenium:selenium-firefox-driver"),
    @Grab("org.seleniumhq.selenium:selenium-support")
])
import geb.Browser
 
Browser.drive {
    go "http://google.com/ncr"
 
    // make sure we actually got to the page
    assert title == "Google"
 
    // enter wikipedia into the search field
    $("input", name: "q").value("wikipedia")
 
    // wait for the change to results page to happen
    // (google updates the page dynamically without a new request)
    waitFor { title.endsWith("Google Search") }
 
    // is the first link to wikipedia?
    def firstLink = $("li.g", 0).find("a.l")
    assert firstLink.text() == "Wikipedia"
 
    // click the link
    firstLink.click()
 
    // wait for Google's javascript to redirect to Wikipedia
    waitFor { title.contains "Wikipedia" }
}.quit()

println "Done!"