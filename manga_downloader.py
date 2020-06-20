
import urllib3
from bs4 import BeautifulSoup
import os
from fpdf import FPDF
from PIL import Image
import sys
import os

def readUrlContent(httpManager, url):
    page = httpManager.urlopen('GET', url)
    return page.data

def createJpgMangaImages(httpManager, pageContent, keyword):
    soup = BeautifulSoup(pageContent, 'html.parser')
    tags = soup.find_all('img')

    i = 0

    # get all of the images urls and create image from content
    for img in tags:
        img_url = img.get('src')
        #if keyword in img_url:
        r = httpManager.urlopen('GET', img_url, preload_content=False)
        image_extension = img_url.split(".")[-1]
        with open(f"{i}.jpg", 'wb') as out:
            while True:
                data = r.read()
                if not data:
                    i += 1
                    break
                out.write(data)

    return i, image_extension

def createPDFFromImages(endIndex, mangaChapter, image_extension):
    pdf = FPDF()

    for j in range(0, endIndex):
        im = Image.open(f"{j}.jpg")
        width, height = im.size

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
        except Exception as e:
            print(e)

    pdf.output(mangaChapter, "F")

def cleanTempFiles():
    current_dir = "."

    # clean folder jpg
    filelist = [ f for f in os.listdir(current_dir) if f.endswith(".jpg") ]
    for f in filelist:
        os.remove(os.path.join(current_dir, f))

def extractNameFromUrl(url):
    splitted_url = url.split('/')
    return f"{splitted_url[-1]}.pdf"

keyword = os.environ['KEYWORD']
url = os.environ['URL']
httpManager = urllib3.PoolManager()
pageContent = readUrlContent(httpManager, url)
lastFileIndex = createJpgMangaImages(httpManager, pageContent, '')
createPDFFromImages(lastFileIndex[0], extractNameFromUrl(url), lastFileIndex[1])
cleanTempFiles()