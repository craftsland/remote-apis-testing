FROM ubuntu:18.04


RUN apt update && apt install -yq git openjdk-11-jdk wget \
    curl gnupg # For curl | apt-key to work

RUN wget -O install-bazel.deb \
    https://github.com/bazelbuild/bazel/releases/download/0.28.1/bazel_0.28.1-linux-x86_64.deb
RUN apt install -yq ./install-bazel.deb && rm install-bazel.deb


RUN apt install -yq git

WORKDIR /src

COPY bazel-build-wrapper-crosstools /bin/bazel-build-wrapper
COPY bazelrc-buildbarn /src/bazelrc
COPY workspace-buildbarn /src/workspace
