FROM python:2
ENV PYTHONUNBUFFERED 1
# install utilities in Debian
RUN apt-get update && apt-get install -y \
    graphicsmagick
# install Django and other dependencies
RUN mkdir -p /webapp/renamer
WORKDIR /webapp
COPY requirements.txt /webapp/
# fix missing templates for django.contrib.admin 
RUN pip install --no-binary Django Django==1.4.3
# install the rest normally
RUN pip install -r requirements.txt

# bring your own kdu_compress!
COPY vendor/kdu_compress /usr/local/bin/
COPY vendor/libkdu_v7AR.so /usr/local/lib/libkdu_v7AR.so
RUN ldconfig

# copy app
COPY renamer /webapp/renamer/
COPY manage.py /webapp/

COPY docker-entrypoint.sh /webapp/
EXPOSE 8000
CMD ["/webapp/docker-entrypoint.sh"]
