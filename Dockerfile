FROM python:3.6.4
ENV HOME /app/oauth2
COPY . $HOME
WORKDIR $HOME

RUN pip install --upgrade pip
RUN pip install peewee
RUN pip install Flask
RUN pip install mysqlclient

RUN pip install uwsgi

RUN chown 995:992 /app -R

USER 995

CMD uwsgi --ini app.ini