import req_func as rf

itpro = {
    'url':'https://www.itpro.com/security'
}

darkreading = {
    'url':'https://www.darkreading.com'
}

thehackernews = {
    'url':'https://www.thehackernews.com'
    }

hackread = {
    'url':'https://www.hackread.com'
}

gbhackers = {
    'url':'https://www.gbhackers.com'
}

talosintelligence = {
    'url':'https://blog.talosintelligence.com'
}

listing = [
    itpro, 
    darkreading, 
    thehackernews,
    hackread, 
    gbhackers, 
    talosintelligence
]

for website in listing:
    print("--- Get data and log_track")
    rf.get_response_content(website)
    rf.log_track_info(website)
    print(f"website : {website['url']}")
    print(f"status code : {website['response'].status_code}")
    print("--- Scraping is completed !")
    print("--- Get file")
    rf.send_to_html_file(website)
    print("--- File is saved !")
    

    
