
import urllib3
from bs4 import BeautifulSoup
import os
from fpdf import FPDF
from PIL import Image

http = urllib3.PoolManager()
page = http.urlopen(
    'GET', 'https://read.mangabat.com/read-dt34668-chap-180')
soup = BeautifulSoup(page.data, 'html.parser')
tags = soup.find_all('img')

i = 0

# get all of the images urls and create image from content
for img in tags:
    img_url = img.get('src')
    print(img_url)
    r = http.urlopen('GET', img_url, preload_content=False)
    with open(f"{i}.jpg", 'wb') as out:
        while True:
            data = r.read()
            if not data:
                break
            out.write(data)
    i += 1

current_dir = "."
pdf = FPDF()

for j in range(0, i):
    im = Image.open(f"{j}.jpg")
    width, height = im.size
    print(f"width: {width} - height: {height}")

    # convert pixel in mm with 1px=0.264583 mm, mm is default for FPDF
    width, height = float(width * 0.264583), float(height * 0.264583)

    # given we are working with A4 format size on pdf
    pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

    orientation = 'P' if width < height else 'L'

    #  make sure image size is not greater than the pdf format size
    width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
    height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']

    try:
        pdf.add_page(orientation=orientation)
        pdf.image(f"{j}.jpg", 0, 0, width, height)
    except:
        print("error reading one of the iamges on fpdf")

pdf.output("yakusoku-180.pdf", "F")

# clean folder jpg
filelist = [ f for f in os.listdir(current_dir) if f.endswith(".jpg") ]
for f in filelist:
    os.remove(os.path.join(current_dir, f))