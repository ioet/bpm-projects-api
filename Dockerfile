FROM ubuntu:18.04
LABEL maintainer="ehernandez@ioet.com"

ARG DB_URI

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python3 python3-dev python3-pip
RUN apt-get install -y curl
RUN apt-get install -y jq

# Add requirements.txt before rest of repo for caching
ADD requirements/*.txt /app/requirements/

WORKDIR /app

RUN pip3 install -r requirements/azure-prod.txt

ADD . /app

ENV FLASK_APP bpm_projects_api
ENV APP_CONFIG bpm_projects_api.config.AzureProductionConfig
ENV FLASK_ENV production
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV DB_URI $DB_URI

# Setup and Run the OPA policies server
RUN make opa-linux
RUN make bpm-opa-directory
RUN make start-opa
EXPOSE 8181

EXPOSE 8000

CMD ["make", "run"]
