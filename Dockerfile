FROM python:3.10
MAINTAINER yurasblv.y@gmail.com
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app
RUN chmod u+x ./entrypoint.sh
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV='development'
EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]

