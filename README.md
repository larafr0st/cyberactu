## About the project

Last fresh version : 2025-02-16

As a beginner, I found it was a funny way to practice python scripting, data
manipulation and data storage.

I wanted to keep track of the mainstream english-speaking cyber news day by 
day. I was curious about who was talking about what eh !  

### External doc

- [venv](https://docs.python.org/3/library/venv.html)
- [subprocess](https://docs.python.org/3/library/subprocess.html)
- [os](https://docs.python.org/3/library/os.html)
- [sqlite3 library](https://docs.python.org/3/library/sqlite3.html)
- [sqlite](https://www.sqlite.org/docs.html)
- [xml etree](https://docs.python.org/3/library/xml.etree.elementtree.html)
- [requests](https://requests.readthedocs.io/en/latest/)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [fun](https://www.python.org/doc/humor/)

## Structure

### Old Stuff : 'old_start' and 'rss' folders

They are not mandatory parts of the actual version but, they stay as an 
artefact of attempts and x-perimental steps. They are reminder 
of Occam's razor, KISS principle, RubberDucky Debug theory, Complex not 
complicated...all that kind of struglglsh1t were real.  

### New Stuff

**main.py** : main code  
**content_files** folder : created for ease if you clone the repo. If not, you
will have to create it in the same directory than the main.py script. This 
folder will contain an xml file for each website. If you want to run it on
windows, you'll have to tweak the paths. 

### Considerations

List is not exhaustive :

*Scrap, crawl, spider, what are the differences ?
What are good practices ? 
Where to find accurate information ? 
How to treat the data ?
What tool for what usage ?
What the doc' says ?
File usage or database ? 
How to standardize data ? 
How to keep track of the process ? 
Why use that function and not that one ? 
Should I use a third-party library ? 
Why does it work ? 
Why doesn't it work ? 
Is this efficient ? 
If it works on my machine, will it work on others ? 
How do python virtual environment work ? 
What to do to handle errors ? 
What could go wrong ? 
How to maintain ? 
Should I bypass 403 ?
What about security ?*  

## Environment

OS : Debian 12 desktop  
Python : version 3.11.2 

### Virtual Environment settings and Python Libraries Configuration 

A virtual environment for python implies that you cannot mess with the current 
system packages and configuration, which sounds great. 
Then in the script, there is a condition to check if the venv already exists or
not, it is installed if it doesn't already exist. Then, it is activated and 
imports third-party library.  

#### Venv as Portal of Despair 

*[...] and imports third-party library*  
I need more time to work on this explanation, I'm still hallucinating about it.
In its current state, there is no issue with Requests because most part of
the time, even though it is not a built-in member, it is already installed
in some linux distro, as system package. 

#### Modules Usage & Security Considerations

- os and subprocess : to create then activate the venv, manage paths
- datetime : for handling dates and times
- sqlite3 : for data storage
- xml.etree : for parsing xml
- requests : for the requests (obviously)

Etree is not s-e-c-u-r-e. XXE, poisoning billion laughs attack & ddos poetry.
[More info about XXE on portswigger](https://portswigger.net/web-security/xxe)  

## Data

### Data Storage

At this point, no need for db gas factory and a .db file from sqlite do the 
work perfectly for data storage. I faced multiple questions and existential 
crisis with this part. Nonetheless, the documentation of sqlite was really 
interesting, even for more 'philosophical' considerations like flexible typing.
More info about it : https://www.sqlite.org/flextypegood.html

The script creates a connection to the db and if 'news.db' doesn't already 
exist, it is automatically created. Then, a table named 'web_content' is 
created, if not already exists, with the next columns : 

- date : publication date
- sitename : where the article comes from
- title : title
- link : URL to access the article

UNIQUE is used to ensure that there will be no duplicates in the content from 
the three columns date, sitename and title. 
Eventually, a 'true false duplicate' can appear. 
True because it is in fact, a duplicate but false because it could
be a hint about an upgraded or modified article. 
In the end, this behavior should not appear with rss/atom because there is a 
dedicated tag to indicate an upgrade of the article.

**send_data(data)**

Connects to the db and creates a cursor. Then, elements of data are
send to the file. The modifications are commited and the connection is finally
closed.  
If the .db is modified, even if it's saved, it will throw a db locked 
error if the file is still opened when the script is running. 

### Data Gathering

Headers are defined and stored into a variable. I don't think that missing
headers could be an issue for rss grabbing. But it is clearly one when you
start to work with source code of a website. Some websites are waiting for a
browser to request them. This is something you can also see when you use curl. 

Each site is a dictionary with two keys : name and url. The url is used to
request data. All the sites are stored into a list to use into the main loop.

**get_content(site, headers)**  

This is the request to gather the data. 
As there is an infinite timeout by default, I set it to 10 seconds. 
It ensures that the script will not be blocked if a website is not responding.
I didn't think of it at first, even though it is a good practice. 
Then it happened once and I had to investigate this issue.  

Nevertheless, ensure that the script will not be blocked by timeout is not 
enough. Why ?  
This case happened with the Cybersecurity Dive website, which threw an error 
522, and caused timeout. The timeout was correctly managed but, as there was no 
content to send, it threw an error into the send_content_file() function. 

```
[ FAIL ] HTTPSConnectionPool(host='www.cybersecuritydive.com', port=443): 
Read timed out. (read timeout=10) [...]
TypeError: write() argument must be str, not None
```
This problem was solved with a condition into the main loop. It checks if the 
content is None or not. If it's not, the next step continue and if it's, it
prints a fail message then continue with other websites.

**send_content_file(site, content)**

Used to send the gathered xml data to a file in the content_files folder.  

Why keep track of files ?  
First, I decided to work with files to avoid too many requests to the website
when testing stuff. Also, it was interesting to have an eye on the structure of
the file's content.
Later,after some readings, I thought that it might not be so smart to keep
the files, as it is apparently slower than working directly from the request 
response. In fact, in this context, the speed is not an issue.

**parsing_data(site)**

Extract data from the xml file by parsing it to obtain the tree and 
gather the root. Define an empty list to stock data. Then, iterate through 
each item in the content and retrieve the title, link and publication date. 
Append these data to the empty list. Finally, return data as a list of lists

### Data Cleaning & Formatting

**cleaning_date(data)**

This one is used to ensure that all the publication dates are formatted in
a same way into the .db file. Datetime style strikes again. The 'formats'
variable contains a list of format date. The two last elements of this list
are ISO-8601 format. 

## Main Loop

For each website, the content is retrieved. If the content is not None, it is
send to a specific file, then data are gathered from the file, cleaned and send
formatted to the db file. If there was a problem with the content gathering of
a particular website, a print output indicates that it went wrong. 

## What's next ? 

[ ] jump to the defusedxml library which [looks like a trusted 
one](https://pypistats.org/packages/defusedxml)  
[ ] add websites with no available rss file  
[ ] CLI display  
[?] GUI display with tkinter  
[ ] gather article's content   
[ ] display article's content
