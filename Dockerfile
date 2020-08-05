FROM python:3.6.5-alpine
RUN echo "http://dl-4.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk update && apk add --no-cache \
    bash \
    openssh \
    git \
    python3-dev \
    gcc


ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /app/requirements.txt
RUN pip freeze
RUN rm /app/requirements.txt
