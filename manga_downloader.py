
import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()
page = http.urlopen(
    'GET', 'https://manganelo.com/chapter/yakusoku_no_neverland/chapter_125')
soup = BeautifulSoup(page.data, 'html.parser')
tags = soup.find_all('img')

i = 0

for img in tags:
    img_url = img.get('src')
    print(img_url)
