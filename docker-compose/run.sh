# The contents of this file are covered by APACHE License Version 2.
# See licenses/APACHEV2-LICENSE.txt for more information.
#
# Runs docker-compose files for server and client REAPI implementations

#!/usr/bin/env bash

set -eu

HELP="""./run.sh - A remote-apis-testing wrapper script
  -s [server]: A path to a docker-compose file which will be spun up to represent the server deployment.
  -c [client]: A path to a docker-compose file which will be spun up to represent the client deployment.
  -a [asset server]: A path to a docker-compose file which will be spun up to represent the asset server deployment.

  -p: Will perform a cleanup of the storage-* directories prior to starting tests. Requires privilege.
"""

# Initialize optional args
ASSET=""
CLEAN=""

while getopts ":s:c:a:p" opt; do
  case ${opt} in
    s ) SERVER="$OPTARG";;
    c ) CLIENT="$OPTARG";;
    a ) ASSET="$OPTARG";;
    p ) CLEAN="TRUE";;
    : ) echo "Missing argument for -$OPTARG" && exit 1;;
    \?) echo "$HELP" && exit 1;;
  esac
done

# Local directory mounted as a volume for the worker
WORKER="worker"
rm -rf $WORKER
mkdir -m 0777 -p $WORKER/{build,cache,remote-execution}

if [[ "$CLEAN" != "" ]]; then
  echo "Performing optional clean"
  rm -rf storage-*
fi

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
