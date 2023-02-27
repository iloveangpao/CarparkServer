FROM python:3.10-alpine

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --without dev

# Creating folders, and files for a project:
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]