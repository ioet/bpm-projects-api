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
RUN curl -o opa https://github.com/open-policy-agent/opa/releases/download/v0.9.2/opa_linux_amd64
RUN chmod 755 ./opa
RUN curl -O $(curl "https://api.github.com/repos/ioet/bpm-opa/releases/latest" | jq -r '.assets[0].browser_download_url')
# Run OPA this way until this issue be solved https://github.com/open-policy-agent/opa/issues/1019
RUN tar -xvzf bpm.tar.gz
RUN ./opa run -s bpm &
EXPOSE 8181


EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "run:app"]
