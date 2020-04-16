FROM ubuntu:18.04
LABEL maintainer="ehernandez@ioet.com"

RUN apt-get update --fix-missing
RUN apt-get install -y python3 python3-dev python3-pip
RUN apt-get install -y curl
RUN apt-get install -y jq

# Add requirements.txt before rest of repo for caching
COPY requirements/*.txt /app/requirements/

WORKDIR /app

RUN pip3 install -r requirements/azure-prod.txt

COPY . /app

ENV FLASK_APP bpm_projects_api
ENV APP_CONFIG bpm_projects_api.config.InMemoryDevelopmentConfig
ENV FLASK_ENV production
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV OPA_SECURED True

# Setup and Run the OPA policies server
RUN make opa-linux
RUN make bpm-opa-directory

EXPOSE 8000
EXPOSE 8180

CMD ["make", "run-with-opa"]
