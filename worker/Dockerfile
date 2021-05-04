FROM python:3.7-slim

COPY . /worker

RUN pip install -r /worker/requirements.txt

RUN chmod +x /worker/wait-for-it.sh