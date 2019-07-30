FROM registry.gitlab.com/buildgrid/buildgrid.hub.docker.com/buildbox:nightly

RUN apt update && apt install -yq python unzip zip
