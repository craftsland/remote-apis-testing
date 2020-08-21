# The contents of this file are covered by APACHE License Version 2.
# See licenses/APACHEV2-LICENSE.txt for more information.
#
# Runs docker-compose files for server and client REAPI implementations

#!/usr/bin/env bash

set -eu

# Initialize optional args
ASSET=""

while getopts ":s:c:a:" opt; do
  case ${opt} in
    s ) SERVER="$OPTARG";;
    c ) CLIENT="$OPTARG";;
    a ) ASSET="$OPTARG";;
    : ) echo "Missing argument for -$OPTARG" && exit 1;;
    \?) echo "./run.sh -s [server] -c [client] -a [asset server]" && exit 1;;
  esac
done

worker="worker"

rm -rf worker
mkdir -m 0777 "${worker}" "${worker}/build"
mkdir -m 0700 "${worker}/cache"

cleanup() {
    EXIT_STATUS=$?
    # Removing $SERVER with orphans will ensure all other
    # services deployed afterwards are removed.
    docker-compose -f $SERVER down --remove-orphans
    exit $EXIT_STATUS
}
trap cleanup EXIT

# Enable buildroot for building images via docker-compose
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

docker-compose -f $SERVER build
docker-compose -f $SERVER up -d
docker-compose -f $SERVER logs --follow &

if [[ "$ASSET" != "" ]]; then
  docker-compose -f $ASSET build
  docker-compose -f $ASSET up -d
  docker-compose -f $ASSET logs --follow &
fi

docker-compose -f $CLIENT build
docker-compose -f $CLIENT up --exit-code-from client
