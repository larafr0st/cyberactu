import requests 
from datetime import datetime

def get_response_content(website):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0'}
    response = requests.get(website['url'], headers=headers)
    website['response'] = response

def log_track_info(website):
    r = website['response']
    log_line = ( 
        f"scrap_time : {datetime.now()}, "
        f"url : {website['url']}, "
        f"status_code : {r.status_code}, "
        f"nbr_char_in_text : {len(r.text)}\n"
    )
    with open('log_file_scrap.txt', 'a') as log_file:
        log_file.write(log_line) 

def gen_html_filename(website):
    site_name = website['url'].split(".")
    html_filename = f"output_{site_name[1]}.html"
    if website['response'].status_code != 200:
        html_filename = f"corrupted_output_{site_name[1]}.html"
    return html_filename

def send_to_html_file(website):
    html_filename = gen_html_filename(website)
    with open(html_filename, 'w') as file:
        file.write(website['response'].text)
