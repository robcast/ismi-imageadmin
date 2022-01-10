FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install utilities in Debian
RUN apt-get update && apt-get install -y \
    graphicsmagick \
    postgresql-client

# install Django and other dependencies
WORKDIR /webapp
COPY requirements.txt /webapp/
RUN pip install -r requirements.txt

# bring your own kdu_compress and put it in ./vendor!
COPY vendor/kdu_compress /usr/local/bin/
COPY vendor/libkdu_v7AR.so /usr/local/lib/libkdu_v7AR.so
RUN ldconfig

# copy app
COPY renamer /webapp/renamer
WORKDIR /webapp/renamer

COPY docker-entrypoint.sh /webapp/
EXPOSE 8000
CMD ["/webapp/docker-entrypoint.sh"]
