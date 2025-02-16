# it's ugly, but it works meeeeeeeeh 
# * gathering data into the mainstream wood *
import requests
import xml.etree.ElementTree as ET

headers = {'user-agent' : 'Mozilla/5.0 Gecko/20100101 Firefox/128.0'}

bleeping = {
    "name": "Bleeping Computer",
    "url": "https://www.bleepingcomputer.com/feed/"
}
thn ={
    "name": "The Hacker News",
    "url": "https://feeds.feedburner.com/TheHackersNews"
}
darkreading = {
    "name": "Dark Reading",
    "url": "https://www.darkreading.com/rss.xml"
}
itpro = {
    "name": "it pro",
    "url": "https://www.itpro.com/feeds/tag/security"
}
krebs = {
    "name": "Krebs on Security",
    "url": "https://krebsonsecurity.com/feed"
}
cybersecuritydive = {
    "name" : "Cybersecurity Dive",
    "url" : "https://www.cybersecuritydive.com/feeds/news"}
    
securitylab = {
    "name" : "Security Lab",
    "url" : "https://www.securitylab.ru/_services/export/rss/"}
    
theregister = {
    "name": "The Register",
    "url" : "https://www.theregister.com/security/headlines.atom"}

# scraping problem 101 : xml parsing error 
# gbhackers = {
#     "name": "GBHackers News",
#     "url": "https://feeds.feedburner.com/gbhackers/cybersecurity"
# }
    
websites = [bleeping, thn, darkreading,itpro, krebs,
cybersecuritydive, securitylab, theregister]

def get_content(url, headers):
    try:
        rss_response = requests.get(url, headers=headers)
        rss_response.raise_for_status()
        return rss_response.content
    except requests.exceptions.HTTPError as http_err:
        print(f"[ FAIL ] {http_err}")
    except Exception as err:
        print(f"[ FAIL ] {err}")
    
def partially_secure_parsing(content):
    # Should call it : "f-e-e-l-i-n-g" of security
    # " Is it secure ? " 
    # " Yeah man, for sure, one hardcoded case only *poke joke* "
    # --> next move : import defusedxml module (later)
    if b'<!DOCTYPE' in content or b'<!ENTITY' in content:
        raise ValueError("[ ALERT ] External entity potentially detected")
    else:
        parsing = ET.fromstring(content)
        return parsing
    
def display_parsing(parsing, site):
    # rss/atom : item/entry
    if site["name"] != 'The Register':
        for item in parsing.findall('./channel/item'):
            title = item.find('title').text
            pub_date = item.find('pubDate').text
            print(f'[ {site["name"]} ] {pub_date[0:25]} : {title}')
    else:
        for entry in parsing.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            pub_date = entry.find('{http://www.w3.org/2005/Atom}published').text
            print(f'[ {site["name"]} ] {pub_date[0:25]} : {title}')

# main
        
for site in websites:
    content = get_content(site["url"], headers)
    parsing = partially_secure_parsing(content)
    display_parsing(parsing, site)
  
