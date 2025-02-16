### Current "issues" & states of mind :
**16-02-2025**

**The Register**  
The register's links contain a inaccurate path part /security/, which causes
a 404 error when the page is requested. 
Also, there was a f%$* thing when 2025 was coming, which caused a temporal 
failure of datetime. As a result, some articles are listed in the db file with 
a datetime of "2025-12-31". Embrace the turfu. Dealing with timestamps is a 
pain in the 4$$, embrace it too. 

**Duplicates**  
But, not really. It appears that some articles are encoded multiple times, 
with a different datetime, into the db. Wtf ? 
In fact, it happens when an article is updated or modified. It is possible 
that, on the website side, the datetime is updated with each modification of
the article's content. Sometimes, it was just a typo correction. 
In some ways, it can be nice, as you are able to track updates of the content. 

**404 error**  
In some cases, I've noticed that some articles disappeared from the
website, resulting in a 404 error when trying to access the page from the link.  
It's interesting, why something disappeared ? 

**403 error**  
I understand, but I hate. By the way, it's a cool way to learn about 
cloudfare's anti-bot measures.

**Wtf are those generated output files**  
Yeah there are useless at the end. 

**Code is bad**  
But I-T W-O-R-K-S. Some parts of the code are overcomplicated for
absolutely no other reason than a skill issue. It needs a good refactoring.

**RSS is the easiest**  
True, but some websites don't work (anymore) with. 
By the way, for the last 7 months, not much trouble has happened and every
change on the websites side was manageable. I'm lying, not all (#lazy). Hacker news is now
returning a 403 error but it still working with rss. Next move is to upgrade the
code to deal with both rss data and website source code when rss is not 
available.
