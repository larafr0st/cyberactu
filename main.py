import subprocess
import os
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime

#-------------------------------------------------------------------------------
# Virtual Environment, Packages Configuration
#-------------------------------------------------------------------------------

# check if env. already exists, if not, create it
env_name = 'env_scrap'
env_path = os.getcwd() + '/env_scrap/bin/activate'
cmd_create_env = f"python3 -m venv {env_name}"

if os.path.exists(env_path):
    print('Virtual env already exists')
else:
    subprocess.run(cmd_create_env, shell=True, executable='/bin/bash')
    print("Virtual env was created")

# activate it
# it will be automatically deactivated at the end of the run
cmd_activate = f"source {env_path}"
subprocess.run(cmd_activate, shell=True, executable='/bin/bash')
print("Virtual env was activated")

# import modules not built-in
try: 
    import requests
except ImportError as e:
    print(f"error:{e}")
    
#-------------------------------------------------------------------------------
# Database Creation
#-------------------------------------------------------------------------------

db_con = sqlite3.connect("news.db")
db_c = db_con.cursor()
query = (
        f"CREATE TABLE IF NOT EXISTS web_content "
        f"(date, sitename, title, link, "
        f"UNIQUE (date, sitename, title))"
        )
db_c.execute(query)
db_con.commit()
db_c.close()

#-------------------------------------------------------------------------------
# Websites dictionaries & parameters for requests
#-------------------------------------------------------------------------------

headers = {'user-agent' : 'Mozilla/5.0 Gecko/20100101 Firefox/128.0'}

bleeping = {
    "name": "Bleeping Computer",
    "url": "https://www.bleepingcomputer.com/feed/"
}
thn ={
    "name": "The Hacker News",
    "url": "https://feeds.feedburner.com/TheHackersNews"
}
# [x] ValueError: time data 'Fri, 14 Feb 2025 18:29:21 GMT' 
# does not match format '%a, %d %b %Y %H:%M:%S %z'
# implemented solution : propose a list of date formats and try till the correct
# one is found
# [ ] some char as : &amp
darkreading = {
    "name": "Dark Reading",
    "url": "https://www.darkreading.com/rss.xml"
}
# [ ] title starts with blank space
itpro = {
    "name": "IT Pro",
    "url": "https://www.itpro.com/feeds/tag/security"
}
krebs = {
    "name": "Krebs on Security",
    "url": "https://krebsonsecurity.com/feed"
}
cybersecuritydive = {
    "name" : "Cybersecurity Dive",
    "url" : "https://www.cybersecuritydive.com/feeds/news"}
    
# there is no time part for hours:minutes:seconds (or they publish at 00:00:00)
trendmicro = {
    "name" : "Trend Micro",
    "url" : "https://feeds.feedburner.com/TrendMicroSimplySecurity"}
    
theregister = {
    "name": "The Register",
    "url" : "https://www.theregister.com/security/headlines.atom"}
    
securelist = {
    "name": "Secure List",
    "url" : "https://securelist.com/feed/"}
    
schneier = {
    "name": "Schneier on Security",
    "url" : "https://www.schneier.com/feed/atom"
}
# returns all the episodes from 2017
# darknetdiaries = {
    # "name": "Darknet Diaries",
    # "url" : "https://podcast.darknetdiaries.com"
# }
websites = [bleeping,
            thn,
            itpro,
            krebs,
            cybersecuritydive,
            trendmicro,
            darkreading,
            theregister,
            securelist,
            schneier]

#-------------------------------------------------------------------------------
# Data Gathering
#-------------------------------------------------------------------------------

# [x] add a timeout for the request 
# about timeout : https://requests.readthedocs.io/en/latest/user/advanced/
def get_content(site, headers):
    try:
        rss_response = requests.get(site['url'], headers=headers, timeout=10)
        rss_response.raise_for_status()
        print(f"[ SUCCESS ] Data are correctly gathered for {site['name']}")
        return rss_response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"[ FAIL ] {http_err}")
    except Exception as err:
        print(f"[ FAIL ] {err}")
        
    
def send_content_file(site, content):
    # The folder 'content_files' should already exists
    filepath_str = f"content_files/{site['name'].replace(' ', '')}.xml"
    with open(filepath_str, 'w') as fw:
        fw.write(content)
        
    
def parsing_data(site):
    ''' Extract data from the xml file by parsing it to obtain the tree and 
    gather the root. Define an empty list to stock data. Then, iterate through 
    each item in the content and retrieve the title, link and publication date. 
    Append these data to the empty list. 
    Finally, return data, which is a list of lists'''
    filepath_str = f"content_files/{site['name'].replace(' ', '')}.xml"
    tree = ET.parse(filepath_str)
    root = tree.getroot()
    data = []
    
    # atom vs rss
    # Note on structure : for the link, it is possible to retrieve a text 
    # element from the rss but, for atom structure, the content is embedded 
    # into a href element and .text doesn't work
    if root.tag == 'rss':
        for item in root.findall('channel/item'):
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            data.append([pub_date, site['name'], title, link])
    elif root.tag == "{http://www.w3.org/2005/Atom}feed":
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            link = entry.find('{http://www.w3.org/2005/Atom}link').get('href')
            pub_date = entry.find('{http://www.w3.org/2005/Atom}published').text
            data.append([pub_date, site['name'], title, link])
    else:
        print(root.tag)
        
    return data
    
#-------------------------------------------------------------------------------
# Data cleaning
#-------------------------------------------------------------------------------

def cleaning_date(data):
    formats = ["%a, %d %b %Y %H:%M:%S %z", 
               "%a, %d %b %Y %H:%M:%S %Z",
               "%Y-%m-%dT%H:%M:%S.%fZ",
               "%Y-%m-%dT%H:%M:%SZ"]
    for each in data:
        date_str = each[0]
        for date_format in formats:
            try:
                date_obj = datetime.strptime(date_str, date_format)
                fmt_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                each[0] = fmt_date
                break
            except ValueError as err:
                continue
                
# [ ] For it pro, the title starts with a blank space, should strip it

#-------------------------------------------------------------------------------
# Data Storage
#-------------------------------------------------------------------------------

def send_data(data):
    db_con = sqlite3.connect("news.db")
    db_c = db_con.cursor()
    query = (
        f"INSERT OR IGNORE INTO web_content "
        f"(date, sitename, title, link) VALUES (?, ?, ?, ?)"
        )
    db_c.executemany(query, data)
    db_con.commit()
    db_c.close()
    
#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

for site in websites:
    content = get_content(site, headers)
    # what could go wrong if timeout ?
    # TypeError: write() argument must be str, not None
    # [x] add condition to check if there is content
    if content is not None:
        send_content_file(site, content)
        items_list = parsing_data(site)
        cleaning_date(items_list)
        # [x] There was a ValueError for darkreading, and the exception was correctly
        # raised, the message was displayed. The data were send to the database and
        # correctly retrieved but, not in the correct format ! 
        # solution : format date list check
        send_data(items_list)
        # for each in items_list:
            # print(each)
    else:
        print(f"[ FAIL ] Data not gathered for {site['name']}")
        
