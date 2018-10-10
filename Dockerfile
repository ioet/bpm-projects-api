FROM ubuntu:18.04
LABEL maintainer="ehernandez@ioet.com"

ARG DB_URI

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python3 python3-dev python3-pip
RUN apt-get install -y curl

# Add requirements.txt before rest of repo for caching
ADD requirements/prod.txt /app/requirements/
ADD requirements/azure-prod.txt /app/requirements/

WORKDIR /app

RUN pip3 install -r requirements/azure-prod.txt

ADD . /app

ENV FLASK_APP bpm_projects_api
ENV APP_CONFIG bpm_projects_api.config.AzureDevelopmentConfig
ENV FLASK_ENV production
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV DB_URI $DB_URI

EXPOSE 8000

CMD ["gunicorn", "-b 0.0.0.0:8000", "run:app"]
