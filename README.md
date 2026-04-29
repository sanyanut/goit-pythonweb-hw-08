# goit-pythonweb-hw-08

### Install project and all dependencies

```
poetry install
```


### Launch build web and db with Docker

```
docker compose up -d --build
``` 

### Make alembic migrations if needed

```
poetry run alembic revision --autogenerate -m "Contacts init"
poetry run alembic upgrade head
```
