FROM python:3.11.3
LABEL authors="juan"

WORKDIR /home/back

RUN mkdir -p .

COPY . .
COPY requirements.txt .
RUN apt-get update -qq && apt-get install ffmpeg libavcodec-extra -y
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]