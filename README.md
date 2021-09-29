# Image processing tool for the ISMI project

Web frontend based on Django.

## Requirements

You need Docker and docker-compose.

## Configuration

```
cp .env.template .env
cp docker-compose.override.yml.template docker-compose.override.yml
```

Edit `.env` and `docker-compose.override.yml` and adjust to your system.

## Run

```
docker-compose up -d
```

Runs image admin server and proxy at port 80 and 443.

The image admin service is available at the URL

http://your.host.name/imageadmin/

## First start

After creating a new empty database run:
```
docker-compose exec webapp python manage.py syncdb
docker-compose exec webapp python manage.py migrate
```
the second command should create a superuser and ask you for the
username and password
```
docker-compose exec webapp python manage.py collectstatic
docker-compose exec webapp cp -r /usr/local/lib/python2.7/site-packages/django/contrib/admin/static/admin renamer/static/
```

Then you should be able to access the Django admin interface with the
superuser at http://your.host.name/imageadmin/admin (where
`your.host.name` is the external host name of your server that you also put in
`VIRTUAL_HOST` in `.env`).

In the Django admin interface you can create additional users for the
image admin service.

## Debugging

To make troubleshooting easier you can access Django directly
at http://localhost:8000/imageadmin/ bypassing the proxy if you enabled the option in
`docker-compose.override.yml`.

Additionally you can set `DEBUG = True` in `renamer/settings.py` to
enable additional debug messages. Do not use this setting in production!

## Notes 

To re-generate all IIIF manifests you can run the generate_iiif_json.py script manually:
```
docker-compose exec webapp python renamer/helpers/generate_iiif_json.py -r /data/image-presentation/data7/srv/images /data/image-presentation/data7/srv/data
```
