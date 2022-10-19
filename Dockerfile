# Docker file para liveness

FROM python:3.9

RUN pip install --upgrade pip

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./app /code/app

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]