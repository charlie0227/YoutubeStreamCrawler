FROM python:3.6
ENV PATH /usr/local/bin:$PATH
COPY . /code
WORKDIR /code
RUN pip3 install -r requirements.txt