# our base image
FROM ubuntu:18.04

RUN mkdir /app
WORKDIR /app

# Install python and pip
RUN apt-get update

ARG V1
ARG V2
ENV V1 ${V1} 
ENV V2 ${V2}
ENV PYTHONIOENCODING utf-8

# Installing dependencies
RUN apt-get install -y apt-utils \
    python \
    python-dev \
    python-pip \
    python3 \
    python3-dev \
    python3-pip \
    libpq-dev \
    build-essential

# upgrade pip
RUN pip install --upgrade pip

# install Python modules needed by the Python integrations
COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r ./requirements.txt

# copy package
COPY ./dev/ ./

ENTRYPOINT ["python3", "main_func.py"]