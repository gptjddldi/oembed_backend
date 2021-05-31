FROM python:3.7
ENV PYTHONUNBURRERED=1

WORKDIR /Oembed
ADD requirements.txt /Oembed

RUN pip3 install -r requirements.txt

ADD . /Oembed/

CMD ["python3", "manage.py", "runserver", "0:8000", "--noreload"]

EXPOSE 8000