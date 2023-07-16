# syntax=docker/dockerfile:1

FROM python:3.11.4-slim-bookworm

WORKDIR /demo

COPY requirements.txt /demo

RUN pip install -r requirements.txt

COPY . /demo

EXPOSE 8000

# FIXME: Make this run properly. It does not work now
CMD [ "uvicorn", "knn3_nl_to_sql.api:app", "--host=0.0.0.0", "--port=8000" ,"--reload" ]
