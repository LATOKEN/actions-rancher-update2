FROM python:3.8-slim
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY rancher-update.py rancher-update.py
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]
