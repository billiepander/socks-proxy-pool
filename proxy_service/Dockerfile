FROM python:3.5

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt && pip install requests[socks]
ADD . /code/

ENTRYPOINT ["python"]

CMD [ "main.py" ]
