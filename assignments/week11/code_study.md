### Template for Code Reading Exercise

1. Where did you find the code and why did you choose it? 

https://github.com/jsvine/waybackpack/tree/master/waybackpack

For my final project I want to create a (maybe animated?) time capsule for websites.
For that I need to scrape archived versions of a webpage --- this is where the 
WayBack Machine comes into play. During my research for the first steps of the 
project I came across this Python command-line tool that lets me download
archived webpages from the WBM (or print a list of URLs). I feel that understanding this code 
well might help me with the next steps of my project. 

---

2. What does the program do? What's the general structure of the program? 

This an example command-line:
```
waybackpack example.com --from-date 20010101 --to-date 20051231'
```
Essentially the programs searches the WBM for all captures of __example.com__ 
between 2001 and 2005. It downloads those HTML files (and optionally CSS/JS/images)
and saves them to folder named by timestamp. 

The program is structured in the following way:

#### 1. asset.py (I will further explain this piece of code)
```
class Asset(object):
    def __init__(self, original_url, timestamp):
```
This code defines an `Asset` class that represents a single archived web page from the WBM.
It handles: 
- Building the archive URL 
- Downloading the HTML 
- Removing WBM-specific UI (basically get a clean HTML)

#### 2. cdx.py
This code interacts with the WBM CDX API to search for archived snapshots of a given URL.
The Wayback Machine's CDX API provides a way to query and filter its vast archive of web pages.
It allows users to search for specific captures based on various criteria like URL, timestamp, and more. 
source: https://en.wikipedia.org/wiki/Wayback_Machine#

#### 3. cli.py
This code enables command-line arguments for (e.g.):
- target URL to archive/download
- output directory or list-only mode
- data ranges, delays, only-uniques, and more

Basically it converts python self-defined modules (the other py. files) into a cmd line utility. 

#### 4. pack.py 
This code defines the `Pack` class, which serves to download multiple archived version of the website. 
It handles batching, file structure and writing clean HTML. 
- searches for snapshots/timestamps of a given URL
- downloads each snapshot's HTML (using .asset)
- saves everything into organized folders 

#### 5. session.py 
This defined a `Session` class to help make web requests like downloading a webpage.
It helps the user safely download web pages by retrying if there's a problem, waiting 
between tries, and telling the user what's happening.
---

3. Function analysis: pick one function and analyze it in detail:

I chose to look at asset.py in more detail because it is the main mechanic behind the whole 
program --- getting the snapshots of a certain URL. 
To understand my explanation it makes sense to also look at the code at the same time 
https://github.com/jsvine/waybackpack/blob/master/waybackpack/asset.py

```
import logging 
import re
from .session import Session
from .settings import DEFAULT_ROOT
```
The first step is to import some python modules. Unfortunately, I still cannot get my head around the
logging module in this context... 
- re: Regular expressions (for matching and cleaning HTML). 
- Session: A helper class for HTTP requests. 
- DEFAULT_ROOT: Base path used in links within cleaned pages.

The WBM serves archived version of web pages using a specific URL format:
`ARCHIVE_TEMPLATE = "https://web.archive.org/web/{timestamp}{flag}/{url}"`

The first part of the Asset Class stores the timestamp and original_url 
and also validates that the timestamp is just numbers:
```
class Asset(object):
    def __init__(self, original_url, timestamp):
        # Ensure timestamp is only numeric
        if re.match(r"^[0-9]+\Z", timestamp) is None:
            raise RuntimeError("invalid timestamp {!r}".format(timestamp))
        self.timestamp = timestamp
        self.original_url = original_url
```
Then there are the following methods:

`def get_archive_url(self, raw=False):`
This method builds the full archive URL. 
Note: The WBM injects its own UI on top of the archived page, i.e. the navigation banner
at the top. Including the `id_` flag instructs the WBM to return the archived content 
exactly as it was (=`raw`). So basically with `raw=True` --> use `id_` flag. Admittedly, I
don't know why the code doesn't directly use the `id_` flag. 

`fetch(self, session=None, raw=False, root=DEFAULT_ROOT)`
This method retrieves the content from the WBM. It creates a helper `Session` object if there hasn't
been one provided yet. It calls `get_archive_url` and using `res = session.get(url)` it makes the
request to download the archived page. 
The code assumes `raw=False` but in case
with `if is_js_redirect:` it checks if it is a redirected page as the page might show "this page moved"
or "try another version" and logs info about the redirect. 
Optionally `if session.follow_redirects:` follows
the redirect and otherwise it skips redirecting completely. 

Finally `if re.search(REMOVAL_PATTERNS[0], content) is not None:` searches for and removes Toolbar HTML, 
injected scripts and other styling. These `REMOVAL_PATTERNS` are defined as a list in the beginning of the code. 
After removing some of the WBM code `if root != "":` checks if the URL still works and adds the full path if necessary.
All in all, this method does all of the heavy lifting.

---
4. Takeaways: are there anything you can learn from the code? (How to structure your code, a clean solution for some function you might also need...)
- seperation of main code functions: although it was a bit confusing in the beginning (because the program is fragmented)
in different files and classes, it makes it easier to understand, test and reuse 
- certain parts of the code for my own project.
- one part of the code deals with how different operating systems might
reject certain characters in file paths, so making sure to handle those exceptions
is something I hadn't thought of before


5. What parts of the code were confusing or difficult at the beginning to understand? Were you able to understand what it is doing after your own research?


-  The use of re.compile() patterns to clean out injected toolbar code seems clever
but I don't think I fully understood it
- how redirect pages were handled (though it made more sense once I looked at actual
examples of redirect pages on the WBM)
- What id_ in the URL meant: I saw it appear in the URL string, but it wasn’t explained in comments. 
I had to look up the Wayback Machine documentation to learn that id_ means “give me the raw page without modifications"
- It took some time to figure out how the classes fit together and get a rough overview 
of the command-line interface connect
