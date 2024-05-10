from scrapy import Selector
import requests
import pandas as pd 

# ##

#template = {
#    'url':'',
#    'xpreq_title':'',
#    'xpreq_time':'',
#    'xpreq_link':''
#}

darkreading = {
    'url':'https://www.darkreading.com', 
    'xpreq_title':'//div[@class="LatestFeatured"]//a[@data-testid = "preview-default-title"]/text()',
    'xpreq_time':'//div[@class="LatestFeatured"]//span[@class = "ListPreview-Date"]/text()',
    'xpreq_link':'//div[@class="LatestFeatured"]//a[@data-testid="preview-default-title"]/@href'
    }
hackernews = {
    'url':'https://www.thehackernews.com', 
    'xpreq_title':'//*/*[@class="home-title"]/text()',
    'xpreq_time':'//*/*[@class="h-datetime"]/text()',
    'xpreq_link':'//*/*[@class="story-link"]/@href'
    }
securityaffairs = {
    'url':'https://www.securityaffairs.com',
    'xpreq_title':'//*[@id="latest_news_section"]//h5[@class="mb-3"]/a/text()',
    'xpreq_time':'//*[@id="latest_news_section"]//div[@class="post-time mb-3"]/span[2]/text()',
    'xpreq_link':'//*[@id="latest_news_section"]//h5[@class="mb-3"]/a/@href'
}
bleepingcomputer = {
    'url':'https://www.bleepingcomputer.com',
    'xpreq_title':'//*[@class="bc_latest_news_text"]//h4/a/text()',
    'xpreq_time':'//*[@class="bc_latest_news_text"]//*[@class="bc_news_date"]/text()',
    'xpreq_link':'//*[@class="bc_latest_news_text"]//h4/a/@href'
}
hackread = {
    'url':'https://www.hackread.com',
    'xpreq_title':'//article//h2/a/text()',
    'xpreq_time':'//*/*[@class="cs-entry__post-meta"]/div[@class="cs-meta-date"]/text()',
    'xpreq_link':'//article//h2/a/@href'
}
gbhackers = {
    'url':'https://www.gbhackers.com',
    'xpreq_title':'//div[@class="item-details"]/h3/a/text()',
    'xpreq_time':'//div[@id="tdi_88"]//div[@class="item-details"]/div[@class="td-module-meta-info"]//time/text()',
    'xpreq_link':'//div[@class="item-details"]/h3/a/@href'
}
talos = {
    'url':'https://blog.talosintelligence.com',
    'xpreq_title':'//div[@class="container p-4 pb-5"]//h2/a/text()',
    'xpreq_time':'//div[@class="container p-4 pb-5"]/span/text()',
    'xpreq_link':'//div[@class="container p-4 pb-5"]//h2/a/@href'
}
itpro = {
    'url':'https://www.itpro.com/security',
    'xpreq_title':'//article//h3[@class="article-name"]/text()',
    'xpreq_time':'//article//p[@class="byline"]//time/text()',
    'xpreq_link':'//div[@data-analytics-id="featured-article"]//a[@class="article-link"]/@href'
}

listing = [
    darkreading,
    hackernews,
    securityaffairs,
    bleepingcomputer,
    hackread,
    gbhackers,
    talos,
    itpro
]

# ##

# to display all content 
pd.set_option('display.max_colwidth', None)

def Get_site_name(url):
    name = url.split('.')
    return name[1]
    
def Get_response(listing):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0'}
    for site in listing:
        site['name'] = Get_site_name(site['url'])
        print(f"connect to...{site['name']}")
        html=requests.get(site['url'], headers=headers).content.decode('utf-8')
        html_content = Selector(text = html)
        site['response'] = html_content
        
def Get_specific_content(listing):
    for site in listing:
        site['title'] = site['response'].xpath(site['xpreq_title']).getall()
        site['time'] = site['response'].xpath(site['xpreq_time']).getall()
        site['link'] = site['response'].xpath(site['xpreq_link']).getall()
    print('scrap content...')
        
def Create_dataframe(listing):
    columns_names = ['time','title','link']
    print('build dataframes...')
    for site in listing:
        zipped = list(zip(site['time'],site['title'],site['link']))
        df = pd.DataFrame(zipped, columns=columns_names)
        check_link = df['link'].str.contains('https')
        if check_link[0] == False:
            df['link'] = site['url'] + df['link']
        print(f"\n{site['name']} : ")
        print(f"\n{df}")

###
Get_response(listing)
Get_specific_content(listing)
Create_dataframe(listing)
###
