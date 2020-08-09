# The contents of this file are covered by APACHE License Version 2.
# See licenses/APACHEV2-LICENSE.txt for more information.

# Base build environment

FROM ubuntu:20.04 AS build_env

RUN apt-get update && apt-get install -y build-essential libyaml-dev

FROM build_env as bazel

ARG BAZEL_VERSION

RUN apt-get update && apt-get install -y wget unzip 
RUN wget -O bazel-installer.sh https://github.com/bazelbuild/bazel/releases/download/$BAZEL_VERSION/bazel-$BAZEL_VERSION-installer-linux-x86_64.sh 
RUN chmod +x bazel-installer.sh 
RUN ./bazel-installer.sh

# Building of buildfarm images (worker and client)

FROM build_env as buildfarm

RUN apt-get update && apt-get install -y wget git unzip

## for apt to be noninteractive
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

## preesed tzdata, update package index, upgrade packages and install needed software
RUN echo "tzdata tzdata/Areas select Europe" > /tmp/preseed.txt; \
    echo "tzdata tzdata/Zones/Europe select Berlin" >> /tmp/preseed.txt; \
    debconf-set-selections /tmp/preseed.txt && \
    apt-get update && \
    apt-get install -y tzdata

RUN apt-get install -y default-jdk
RUN wget -O bazel-installer.sh https://github.com/bazelbuild/bazel/releases/download/3.3.1/bazel-3.3.1-installer-linux-x86_64.sh && chmod +x bazel-installer.sh && ./bazel-installer.sh

RUN git clone https://github.com/bazelbuild/bazel-buildfarm.git
WORKDIR bazel-buildfarm

ARG BUILDFARM_VERSION
RUN git checkout $BUILDFARM_VERSION

RUN bazel build //src/main/java/build/buildfarm/...

ARG BUILDFARM_DAEMON
ENV BUILDFARM_DAEMON_ENV=$BUILDFARM_DAEMON
ARG BUILDFARM_CONFIG
ENV BUILDFARM_CONFIG_ENV=$BUILDFARM_CONFIG
ENTRYPOINT bazel-bin/src/main/java/build/buildfarm/$BUILDFARM_DAEMON_ENV $BUILDFARM_CONFIG_ENV

# Building of buildbox images, using the base build environment

FROM build_env as buildbox

WORKDIR /tmp

ARG BUILDBOX_VERSION
ARG BUILDBOX_HOST_TOOLS_SHA=3f4c2172cf2d5e969ab4ba57b3ed660d5eaedd18

## for apt to be noninteractive
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

## preseed tzdata, update package index, upgrade packages and install needed software
RUN echo "tzdata tzdata/Areas select Europe" > /tmp/preseed.txt; \
    echo "tzdata tzdata/Zones/Europe select Berlin" >> /tmp/preseed.txt; \
    debconf-set-selections /tmp/preseed.txt && \
    apt-get update && \
    apt-get install -y tzdata

RUN \
	apt-get update \
	&& \
	apt-get install -y \
		build-essential git cmake pkg-config \
		libssl-dev libfuse3-dev uuid-dev \
		libprotobuf-dev protobuf-compiler \
		libgrpc-dev libgrpc++-dev protobuf-compiler-grpc \
		libgtest-dev libgmock-dev \
		python3 python3-pip \
		bubblewrap \
	&& \
	apt-get clean

RUN \
	git clone --depth=1 --branch $BUILDBOX_VERSION \
		https://gitlab.com/BuildGrid/buildbox/buildbox-common.git \
		/tmp/buildbox-common \
	&& \
	cmake -B /tmp/buildbox-common/build /tmp/buildbox-common \
		-DBUILD_TESTING=OFF \
	&& \
	make -C /tmp/buildbox-common/build install \
	&& \
	rm -rf /tmp/buildbox-common

RUN \
	git clone --depth=1 \
		https://gitlab.com/BuildGrid/buildbox/buildbox-run-hosttools.git \
		/tmp/buildbox-run-hosttools && cd /tmp/buildbox-run-hosttools && git checkout 3f4c2172cf2d5e969ab4ba57b3ed660d5eaedd18 && cd - \
	&& \
	cmake -B /tmp/buildbox-run-hosttools/build /tmp/buildbox-run-hosttools \
		-DBUILD_TESTING=OFF \
	&& \
	make -C /tmp/buildbox-run-hosttools/build install \
	&& \
	rm -rf /tmp/buildbox-run-hosttools

RUN \
	git clone --depth=1 --branch $BUILDBOX_VERSION \
		https://gitlab.com/BuildGrid/buildbox/buildbox-worker.git \
		/tmp/buildbox-worker \
	&& \
	cmake -B /tmp/buildbox-worker/build /tmp/buildbox-worker \
		-DBUILD_TESTING=OFF \
	&& \
	make -C /tmp/buildbox-worker/build install \
	&& \
	rm -rf /tmp/buildbox-worker

ENTRYPOINT ["buildbox-worker"]

# Building of buildgrid image

FROM ubuntu:20.04 as buildgrid

RUN apt-get update && apt-get install -y git python3 python3-pip

RUN git clone https://gitlab.com/BuildGrid/buildgrid.git
WORKDIR buildgrid

ARG BUILDGRID_VERSION
RUN git checkout $BUILDGRID_VERSION
RUN python3 -m pip install --upgrade setuptools pip wheel
RUN python3 -m pip install --requirement requirements/requirements.db.txt

RUN python3 -m pip install --editable .

ENTRYPOINT ["bgd", "server"]
