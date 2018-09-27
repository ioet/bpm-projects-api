FROM ubuntu:18.04
LABEL maintainer="ehernandez@ioet.com"

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python3 python3-dev python3-pip
RUN apt-get install -y curl

# Add requirements.txt before rest of repo for caching
ADD requirements/prod.txt /app/requirements/

WORKDIR /app

RUN pip3 install -r requirements/prod.txt

ADD . /app

ENV FLASK_APP bpm_projects_api
ENV FLASK_ENV production
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8


EXPOSE 8000

CMD ["gunicorn", "-b 0.0.0.0:8000", "run:app"]
