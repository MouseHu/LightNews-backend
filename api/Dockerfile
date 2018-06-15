FROM python:3.6.2

LABEL maintainer zyli
ENV PYTHONUNBUFFERED 1
RUN mkdir /docker_api
WORKDIR /docker_api
COPY ./requirements.txt /

# RUN pip install -r requirements.txt
RUN pip install -r /requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple  
RUN python -c "import nltk;nltk.download('wordnet')"
