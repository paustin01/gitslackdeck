FROM python:3.7.10-slim-stretch

RUN apt-get update \
    && apt-get install -y zip git curl ntp \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://releases.hashicorp.com/packer/1.7.4/packer_1.7.4_linux_amd64.zip \
    -o packer_1.7.4_linux_amd64.zip \
    && unzip packer_1.7.4_linux_amd64.zip \
    && mkdir -p /usr/local/packer \
    && mv packer /usr/local/packer/ \
    && rm packer_1.7.4_linux_amd64.zip

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY notifier.py /
