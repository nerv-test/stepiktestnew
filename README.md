
## Configuration
Configuration is stored in `src/app/.env`, for examples see `src/app/.env.ci`

## Installing on a local machine
This project requires Python 3.6, PostgreSQL and Redis.

You can run required infrastructure (PostgreSQL and Redis) using docker-compose.

```sh
docker-compose up -d
```

## Development

When developing locally, we use:

- [`poetry`](https://github.com/sdispater/poetry) (**required**)

Install requirements:

```sh
poetry install
cp src/app/.env.ci src/app/.env  # default environment variables
```

Install wkhtmltopdf:

```sh
# MacOS
Dowload release 0.12.3 from here: https://github.com/wkhtmltopdf/wkhtmltopdf/releases/0.12.3/
Install it
```


Testing:

```sh
pytest # unit tests
```

Development servers:

```sh
./manage.py runserver  # development backend
```
