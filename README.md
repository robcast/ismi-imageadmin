# Image processing tool for the ISMI project

Web frontend based on Django.

## Requirements

You need Docker and docker-compose.

## Configuration

```
cp .env.template .env
```

Edit `.env` and adjust to your system.

## Run

```
docker-compose up -d
```

Runs image server and proxy at port 80 and 443.

## Notes

After creating a new empty database run:
```
docker-compose exec webapp python manage.py syncdb
docker-compose exec webapp python manage.py migrate
```

To re-generate all IIIF manifests you can run the generate_iiif_json.py script manually:
```
docker-compose exec webapp python renamer/helpers/generate_iiif_json.py -r /data/image-presentation/data7/srv/images /data/image-presentation/data7/srv/data
```
