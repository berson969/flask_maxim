FROM python:3.8

WORKDIR .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Установка curl и wait-for-it
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /usr/bin/wait-for-it
RUN chmod +x /usr/bin/wait-for-it


COPY . .

EXPOSE 5001