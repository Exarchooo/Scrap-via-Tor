# Scrap-via-Tor
Scrap *not onion* search results via Tor without proxy

Scrap the results of DuckDuckGo with MrMagic!
MrMagic is a free app that allows fully anonymous scraping.
By using the Tor network, you don't need paid and unreliable proxies.
The program allows advanced searching by phrase, header, date range and (many!) websites in one search. 

Pros:

- Free
- Advanced search syntax
- Anonymity
- Ease of use
- Very low detection rate

Cons:

- Average speed (Selenium need to scroll down to click 'load more results')
- If the site has a geolocation blocker, the program will not bypass it
- Works only with duckduckgo engine
- Interface from the 20th century


Requirements:

- Tor Browser
- Mozilla Firefox
- Python


How to install:

1) Click on the right side of this page 'Release'
2) Download MrMagic.ZIP
3) Unzip
4) *In the folder where you unzipped the zip*  Click the explorer's path --> CMD --> pip install requirements.txt
5) Open Tor and connect to the network.
6) Open MrMagic.exe
7) Scrap 


Troubleshooting:

Missed component via terminal - pip install 'component'  
No results despite no errors - copy the link from gecko (firefox) to your browser.
If there are still no results, it means you should use a less demanding syntax.
Blocked page - geolocation blocker or advanced captcha or drm. Or sign in requirment like in Linkedin or Twitter.
App may freeze or doesn't work in more than 1 scrap, so then close and open again
Note: For example; in central/eastern Europe, most of the servers hosting the tor network are in Germany, so you will usually have a German IP.
In other countries can be other issue. Not in the United States. Read more about *Tor's Directory Authorities* to understand. 
This is random, so geo-blocking can be annoying. Despite scraping again, you may have the same country's IP again.
You can also add to the code more agressive lines like a "scrap this page no matter of the number of attempts", however it will slow down a procces of scraping.

Other: update firefox, tor, check tor's connection, check port in tor, install Gecko Driver, change file locations, just try to experiment.

More advanced:
The  uBlock tool is a bit experimental, tested on small scraps.
You can remove the related lines from the python file and try to run via terminal.

Privacy:

If the Tor connection is interrupted, the program will stop working.
Your Tor identity is renewed with each page while scraping. 
Example: duckduckgo showed 3 results:
123.com - New identity
123.com/todaysnews/losangeles - New identity
321.com - New identity
New identity = new IP and proxy

If you're freaky about your anonymity because you scrapping 'big fishes' pages, you can use vpn, app will work normally.
Of course, it's useless on a tor web, but if you *must*  then I recommend mullvad with daita, no logs, kill switch, quantum resistant.
Mullvad send me a cash for this ad please.


I encourage you to report problems.

*Feel free to contribute  <3*
Anti-Captcha solution is needed.

If the program satisfies your needs and you have saved money on buying a proxy, please consider a small donation to: buymeacoffee.com/Exarchooo
