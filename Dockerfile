FROM python:3.10-alpine

# Copy only requirements to cache them in docker layer
WORKDIR /code/

RUN apk update 

COPY poetry.lock pyproject.toml docker-entrypoint.sh alembic.ini /code/
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --without dev

# Creating folders, and files for a project:
COPY ./app /code/app
COPY ./db /code/db
COPY . /code/

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
RUN chmod +x ./docker-entrypoint.sh
# ENTRYPOINT ["./docker-entrypoint.sh"]