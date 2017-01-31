# misc
## dump_depthcore_image_list.py

This mostly works probably ;-) I got tired and stopped working on it. Currently it loops through 17 of the chapters without problems but then it errors out with:

	Progress: 16/45
      [####################################]  100%
	Progress: 17/45
	Traceback (most recent call last):
	  File "C:\Users\Albert Eardley\Desktop\depthcore\print_images.py", line 99, in <module>
	    chapterImageTitleList = pageTree.xpath('/html/body/div[2]/div/div[3]/div[position()>1]/div[*]/h2/text()')
	  File "src\lxml\lxml.etree.pyx", line 1587, in lxml.etree._Element.xpath (src\lxml\lxml.etree.c:59353)
	  File "src\lxml\xpath.pxi", line 307, in lxml.etree.XPathElementEvaluator.__call__ (src\lxml\lxml.etree.c:171227)
	  File "src\lxml\xpath.pxi", line 230, in lxml.etree._XPathEvaluatorBase._handle_result (src\lxml\lxml.etree.c:170213)
	  File "src\lxml\extensions.pxi", line 623, in lxml.etree._unwrapXPathObject (src\lxml\lxml.etree.c:164273)
	  File "src\lxml\extensions.pxi", line 657, in lxml.etree._createNodeSetResult (src\lxml\lxml.etree.c:164711)
	  File "src\lxml\extensions.pxi", line 678, in lxml.etree._unpackNodeSetEntry (src\lxml\lxml.etree.c:164919)
	  File "src\lxml\extensions.pxi", line 804, in lxml.etree._buildElementStringResult (src\lxml\lxml.etree.c:166409)
	  File "src\lxml\apihelpers.pxi", line 1409, in lxml.etree.funicode (src\lxml\lxml.etree.c:31067)
	UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe4 in position 2: invalid continuation byte

I tried to leave some good comments.

### Python libraries required (pip install x)
* requests
* lxml
* roman
* click

I think json and datetime are built in.

The purpose of this script is just to dump a JSON object of all the available images. I do this because everytime you run the script you are slamming their server with request and downloads. This is a pure scrape and as such has to download a webpage for each request. That is Overall Works Page + Each Chapter Page + Each Image Page + Each Image = LOTS OF PAGES.

However, once this script can go all the way through then you will have a JSON file with all the info you need to grab each image from the server and tag it with the info from the JSON file (once the download script is working that is, I suggest limiting the number of images you try to download at first until you are sure that part works).

To load up the JSON file for the script that will download each image and store it just use (or whatever you call the file):

	with open('full_dump_20170131.txt') as jsondump:
		releases = json.load(jsondump)

### Very useful links
* [Click Progressbar Library](http://click.pocoo.org/5/utils/)
* [XPath Stuff Used for dev](http://stackoverflow.com/questions/17380869/get-list-items-inside-div-tag-using-xpath)
* [datetime formatting](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)
* [datetime formatting example](http://stackoverflow.com/questions/2265357/parse-date-string-and-change-format)
* [Converting Roman Numerals](http://stackoverflow.com/questions/19308177/converting-roman-numerals-to-integers-in-python)
* [Basic tool for looking at JSON](http://jsonviewer.stack.hu/)
* [More XPath Stuff](http://www.w3schools.com/xml/xpath_syntax.asp)
* [What started it all lxml](http://docs.python-guide.org/en/latest/scenarios/scrape/#web-scraping)
