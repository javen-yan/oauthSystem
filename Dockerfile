FROM python:3.6.4
ENV HOME /app/oauth2
COPY . $HOME
WORKDIR $HOME

RUN pip install --upgrade pip
RUN pip install peewee
RUN pip install Flask
RUN pip install mysqlclient

RUN pip install uwsgi

RUN chown root:root /app -R

USER root

CMD uwsgi --ini app.ini