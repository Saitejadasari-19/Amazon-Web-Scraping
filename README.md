<h1>Scraping of Amazon Products</h1>

<p>In this Project we are scraping about product details based on the keyword search</p>

<h3>What is web scraping?</h3>
<p>Web scraping is the process of extracting content and data from a website</p>

<h3>Things required for scraping</h3>
<ul>
<li>Requests Module: The requests module allows you to send HTTP requests using Python.The HTTP request returns a Response Object with all the response data (content, encoding, status, etc).If status_code == 200 then our page downloaded sucessfully else there is an issue in downloading the page. 
To install requests library we use $ python -m pip install requests</li>
<li>Beautiful Soup Module: Beautiful Soup is a Python library for pulling data out of HTML and XML files. Beautiful Soup transforms a complex HTML document into a complex tree of Python objects.
To install BeautifulSoup we can use $ python -m pip install beautifulsoup4</li>
<li>Set of User Agents: User agent helps us with the end-user interaction with web content. The user agent string helps the destination server identify which browser, type of device, and operating system is being used. If you are making a large number of requests for web scraping a website, it is a good idea to randomize. You can make each request you send look random, by changing the exit IP address of the request using rotating proxies and sending a different set of HTTP headers to make it look like the request is coming from different computers from different browsers.</li>
</ul>