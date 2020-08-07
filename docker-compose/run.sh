# The contents of this file are covered by APACHE License Version 2.
# See licenses/APACHEV2-LICENSE.txt for more information.
#
# Runs docker-compose files for server and client REAPI implementations

#!/usr/bin/env bash

set -eu

while getopts ":s:c:" opt; do
  case ${opt} in
    s ) SERVER="$OPTARG";;
    c ) CLIENT="$OPTARG";;
    : ) echo "Missing argument for -$OPTARG" && exit 1;;
    \?) echo "./run.sh -s [server] -c [client]" && exit 1;;
  esac
done

worker="worker"

rm -rf worker
mkdir -m 0777 "${worker}" "${worker}/build"
mkdir -m 0700 "${worker}/cache"

cleanup() {
    EXIT_STATUS=$?
    docker-compose -f $SERVER down 
    docker-compose -f $CLIENT down 
    exit $EXIT_STATUS
}
trap cleanup EXIT

docker-compose -f $SERVER build
docker-compose -f $SERVER up -d
docker-compose -f $SERVER logs --follow &

docker-compose -f $CLIENT build
docker-compose -f $CLIENT up --exit-code-from client


