FROM ubuntu:20.04

RUN apt-get update && apt-get install -y git python3 python3-pip

RUN git clone https://gitlab.com/BuildGrid/buildgrid.git
WORKDIR buildgrid

ARG BUILDGRID_VERSION
RUN git checkout $BUILDGRID_VERSION
RUN python3 -m pip install --upgrade setuptools pip wheel
RUN python3 -m pip install --requirement requirements/requirements.db.txt

RUN python3 -m pip install --editable .

ENTRYPOINT ["bgd", "server"]
