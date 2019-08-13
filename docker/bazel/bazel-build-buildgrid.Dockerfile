FROM debian:buster


RUN apt update && apt install -yq git openjdk-11-jdk wget \
    curl gnupg # For curl | apt-key to work

RUN wget -O install-bazel.deb \
    https://github.com/bazelbuild/bazel/releases/download/0.28.1/bazel_0.28.1-linux-x86_64.deb
RUN apt install -yq ./install-bazel.deb && rm install-bazel.deb

RUN apt install -yq git clang

WORKDIR /src

COPY bazel-build-wrapper-host /bin/bazel-build-wrapper
COPY bazelrc-host /src/bazelrc
COPY workspace-host /src/workspace
