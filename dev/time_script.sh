#!/bin/bash
usage() {
  echo Usage: time_script.sh RE_NAME CLIENT_NAME JOB_NAME
  exit 1
}

if [ $# -ge 3  ]
then
  case $2 in
    bazel)
      time=$(kubectl -n $1 logs --tail=10 jobs/$3 | sed -n -e s/,//g -e '/^INFO: Elapsed time:/p' | awk '{ print $4 }')
      ;;
      echo $time
      ;;
    *)
      echo Client not currently supported
      exit 1
      ;;
  esac
else
  echo Missing arguments
  usage
fi
