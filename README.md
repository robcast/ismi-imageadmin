# Image processing tool for the ISMI project

Web frontend based on Django 4.

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
docker-compose exec webapp python manage.py migrate
docker-compose exec webapp python manage.py createsuperuser
```

the second command should create a superuser and ask you for the
username and password. Then run

```
docker-compose exec webapp python manage.py collectstatic
```

After that you should be able to access the Django admin interface and log in 
at http://your.host.name/admin (where
`your.host.name` is the external host name of your server that you also put in
`VIRTUAL_HOST` in `.env`) using the superuser you just created .

In the Django admin interface you should create additional users for the
image admin service.

## Debugging

To make troubleshooting easier you can access Django directly
at http://localhost:8000/imageadmin/ bypassing the proxy if you enable the optional ports in
`docker-compose.override.yml`.

Additionally you can set `DEBUG = True` in `renamer/settings.py` and `RUN_MODE=development`
and `RUN_LOG_LEVEL=DEBUG` in `.env` to
enable additional debug messages. Do not use these settings in production!

## Notes 

To re-generate all IIIF manifests you can run the generate_iiif_json.py script manually:

```
docker-compose exec webapp python imageadmin/helpers/generate_iiif_json.py -r /data/image-presentation/data7/srv/images /data/image-presentation/data7/srv/data
```
