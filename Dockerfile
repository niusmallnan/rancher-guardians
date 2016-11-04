FROM python:2.7.12-alpine

MAINTAINER niusmallnan <zhangzhibo521@gmail.com>

RUN mkdir ~/.pip
ADD .pip.aliyun.conf ~/.pip/pip.conf

RUN mkdir -p /app
WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["./main.py"]
