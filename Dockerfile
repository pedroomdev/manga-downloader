FROM python:3.7-slim

WORKDIR /app

# both files are explicitly required!
COPY manga_downloader.py requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python", "manga_downloader.py"]