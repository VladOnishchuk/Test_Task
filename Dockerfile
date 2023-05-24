# pull official base image
FROM python:3.9.6-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install build dependencies
RUN apt-get update && apt-get install -y build-essential

# update pip
RUN pip install --upgrade pip && \
    pip install -U spacy && \
    python -m spacy download en_core_web_sm

# install dependencies

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
