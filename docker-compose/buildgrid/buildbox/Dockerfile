FROM ubuntu:20.04

WORKDIR /tmp

ARG BUILDBOX_VERSION
ARG BUILDBOX_HOST_TOOLS_SHA=3f4c2172cf2d5e969ab4ba57b3ed660d5eaedd18

## for apt to be noninteractive
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

## preesed tzdata, update package index, upgrade packages and install needed software
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