FROM ubuntu:18.04
LABEL maintainer="ehernandez@ioet.com"

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python3 python3-dev python3-pip

COPY . /app
WORKDIR /app

ENV FLASK_APP bpm_projects_api

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3", "-m" ]

CMD ["flask", "run"]