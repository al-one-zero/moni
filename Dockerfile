FROM python:latest

EXPOSE 8080

ADD requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app

RUN useradd appuser && chown -R appuser /app
USER appuser