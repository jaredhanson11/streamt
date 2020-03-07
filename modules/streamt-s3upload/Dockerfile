FROM python:3.7-alpine

WORKDIR /app

# Install required packages
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache -r requirements.txt \
    && rm requirements.txt

COPY ./upload_videos.py /app/upload_videos.py
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]
