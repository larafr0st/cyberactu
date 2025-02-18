import req_func as rf

itpro = {
    'url':'https://www.itpro.com/security',
    'xpreq_title':'//article//h3[@class="article-name"]/text()',
    'xpreq_time':'//article//p[@class="byline"]//time/text()',
    'xpreq_link':'//div[@data-analytics-id="featured-article"]//a[@class="article-link"]/@href'
    }
darkreading = {
    'url':'https://www.darkreading.com', 
    'xpreq_title':'//div[@class="LatestFeatured"]//a[@data-testid = "preview-default-title"]/text()',
    'xpreq_time':'//div[@class="LatestFeatured"]//span[@class = "ListPreview-Date"]/text()',
    'xpreq_link':'//div[@class="LatestFeatured"]//a[@data-testid="preview-default-title"]/@href'
    }
thehackernews = {
    'url':'https://www.thehackernews.com', 
    'xpreq_title':'//*/*[@class="home-title"]/text()',
    'xpreq_time':'//*/*[@class="h-datetime"]/text()',
    'xpreq_link':'//*/*[@class="story-link"]/@href'
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
talosintelligence = {
    'url':'https://blog.talosintelligence.com',
    'xpreq_title':'//div[@class="container p-4 pb-5"]//h2/a/text()',
    'xpreq_time':'//div[@class="container p-4 pb-5"]/span/text()',
    'xpreq_link':'//div[@class="container p-4 pb-5"]//h2/a/@href'
    }
cybersecuritynews = {
    'url':'https://www.cybersecuritynews.com',
    'xpreq_title':'//div[@id="tdi_20"]//div[@class="item-details"]//a/@title',
    'xpreq_time':'//div[@id="tdi_20"]//div[@class="item-details"]//div[@class="td-module-meta-info"]//span[@class="td-post-date"]//time/text()',
    'xpreq_link':'//div[@id="tdi_20"]//div[@class="item-details"]//a/@href'
    }
secmag = {
    'url':'https://www.securitymagazine.com/topics/2236-cybersecurity-news',
    'xpreq_title':'//div[@class="article-summary__details has-image"]//a[@class="more"]/@title',
    'xpreq_time':'//div[@class="article-summary__details has-image"]//div[@class="post-meta"]//div[@class="date article-summary__post-date"]/text()',
    'xpreq_link':'//div[@class="article-summary__details has-image"]//a/@href'
    }
trendmicro = {
    'url':'https://www.trendmicro.com/vinfo/be/security/news',
    'xpreq_title':'//div[@class="list_Content"]//div[@class="titlelist"]//a/text()',
    'xpreq_time':'//div[@class="list_Content"]//div[@class="datePubSmall"]/text()',
    'xpreq_link':'//div[@class="list_Content"]//div[@class="titlelist"]//a/@href'
    }
theregister = {
    'url':'https://www.theregister.com/security',
    'xpreq_title':'//div[@class="headlines"]//article//a[@class="story_link"]//h4/text()',
    'xpreq_time':'//div[@class="headlines"]//article//a[@class="story_link"]//div[@class="time_comments"]//span[@class="time_stamp"]/@title',
    'xpreq_link':'//div[@class="headlines"]//article//a[@class="story_link"]/@href'
    }
helpnetsecurity = {
    'url': 'https://www.helpnetsecurity.com/',
    'xpreq_title': '//div[@class="card-body border-bottom-1 mb-3"]//a/@title',
    'xpreq_time': '//div[@class="card-body border-bottom-1 mb-3"]//time/text()',
    'xpreq_link': '//div[@class="card-body border-bottom-1 mb-3"]//a/@href'
    }
bleepingcomputer = {
    'url':'https://www.bleepingcomputer.com',
    'xpreq_title':'//*[@class="bc_latest_news_text"]//h4/a/text()',
    'xpreq_time':'//*[@class="bc_latest_news_text"]//*[@class="bc_news_date"]/text()',
    'xpreq_link':'//*[@class="bc_latest_news_text"]//h4/a/@href'
}
listing = [
    itpro, 
    darkreading, 
    thehackernews,
    hackread, 
    gbhackers, 
    talosintelligence,
    cybersecuritynews,
    secmag,
    trendmicro,
    theregister,
    helpnetsecurity,
    bleepingcomputer
]

for site in listing:
    rf.gen_sitename(site)
    print("--- Get data and log_track")
    rf.get_response_content(site)
    rf.log_track_info(site)
    print(f"site : {site['url']}")
    print(f"status code : {site['response'].status_code}")
    print("--- Scraping is completed !")
    rf.write_to_html_file(site)
    rf.extract_content(site)
    print("--- html text content saved into file !")
    print("--- Format stuff and send to database")
    rf.create_table()
    rf.format_date(site)
    rf.format_link(site)
    rf.insert_data_to_table(site)

