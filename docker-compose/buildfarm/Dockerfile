FROM ubuntu:20.04

RUN apt-get update && apt-get install -y wget git build-essential
RUN apt-get install -y unzip

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
