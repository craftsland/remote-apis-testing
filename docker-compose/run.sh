#!/usr/bin/env bash
# The contents of this file are covered by APACHE License Version 2.
# See licenses/APACHEV2-LICENSE.txt for more information.
#
# Runs docker-compose files for server and client REAPI implementations

set -eu

HELP="""./run.sh - A remote-apis-testing wrapper script
  -s [server]: A path to a docker-compose file which will be spun up to represent the server deployment.
  -c [client]: A path to a docker-compose file which will be spun up to represent the client deployment.
  -a [asset server]: A path to a docker-compose file which will be spun up to represent the asset server deployment.
  -d [name]: Dumps the data for this run with a given name. This can be later used in the static site and is of the format {client}+{server}.
  -u [url]: If specified with the -d flag, the provided url is included in the job_url field in the json output.

  -p: Will perform a cleanup of the storage-* directories prior to starting tests. Requires privilege.
"""

# Initialize optional args
ASSET=""
CLEAN=""
JOB_NAME=""
JOB_URL=""

while getopts ":s:c:a:d:u:p" opt; do
  case ${opt} in
    s ) SERVER="$OPTARG";;
    c ) CLIENT="$OPTARG";;
    a ) ASSET="$OPTARG";;
    d ) JOB_NAME="$OPTARG";;
    u ) JOB_URL="$OPTARG";;
    p ) CLEAN="TRUE";;
    : ) echo "Missing argument for -$OPTARG" && exit 1;;
    \?) echo "$HELP" && exit 1;;
  esac
done

# Local directory mounted as a volume for the worker
WORKER="worker"

# bb is a directory created by buildbarn deployments and should be removed
# at the start of every buildbarn deployment to prevent ETXTBSY errors from occurring.
# If -p is set this effectively gives a clean environment akin to CI runs.
rm -rf $WORKER bb

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

    if [[ "$JOB_NAME" != "" ]]; then
      PASS=$([ "$EXIT_STATUS" == 0 ] && echo "true" || echo "false")

      # Add the job url so that the static site can link
      # to the exact job that created a given result
      JOB_URL_ARG=$([ "$JOB_URL" != "" ] && echo ", \"job_url\": \"$JOB_URL\"" || echo "")
      echo "{ \"pass\": $PASS, \"name\": \"$JOB_NAME\"$JOB_URL_ARG }"
    fi

    exit $EXIT_STATUS
}
trap cleanup EXIT

# Enable buildroot for building images via docker-compose
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

{
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
} 1>&2
