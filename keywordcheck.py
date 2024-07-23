import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

def robot_block(url):
    try:
        # Parse the URL to get the base URL
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # Check the robots.txt file
    
        robots_url = f"{base_url}/robots.txt"
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        if not rp.can_fetch("*", url):
            return True
    except:
        pass
    return False

def response_code(url):
    # Check the HTTP response code
    try:
        response = requests.get(url, verify=False)
        if response.status_code != 200:
            print(f"Invalid response code {response.status_code} for URL: {url}")
            return True
    except:
        pass
    return False


def checkContent (keyword, url):
    if robot_block(url):
        return {"error" : "URL geblokkeerd door Robots.txt"}
    if response_code(url):
        return {"error" : "URL wordt omgeleid of niet gevonden"}
    kw = unidecode(keyword)
    kw = kw.lower()
    url_path = unidecode(keyword.replace(' ', '-'))
    url_path = url_path.replace("", '')
    if url_path in url.lower():
        kw_in_url = True
    else:
        kw_in_url = False
    soup = BeautifulSoup(requests.get(url, verify=False).content, 'html.parser', from_encoding="iso-8859-8")
    title = soup.title.text.lower()
    title = title.replace('.','')
    title = title.replace('-', ' ')
    title = unidecode(title)
    if kw in title:
        kw_in_title = True
    else:
        kw_in_title = False
    header = soup.find('h1')
    header = str(header).lower()
    header = header.replace('.', '')
    header = header.replace('-', ' ')
    header = unidecode(header)
    if kw in header:
        kw_in_header = True
    else:
        kw_in_header = False
    text = soup.get_text()
    text = text.lower()
    text = text.replace('.', '')
    text = text.replace('-', ' ')
    text = unidecode(text)
    keyword_count = text.count(kw)
    return {"url" : kw_in_url, "title": kw_in_title, "header" : kw_in_header, "count": keyword_count}
