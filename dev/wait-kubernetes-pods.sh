#! /bin/bash

if [ "$#" -eq 1 ]
then
      until kubectl -n "$1" get pods --field-selector=status.phase!=Running 2>&1 | grep -q -e "No resources found."
        do
                kubectl -n "$1" get pods
                if kubectl -n "$1" get pods --field-selector=status.phase==Failed 2>&1 | grep -q -v "No resources found."
                then
                        exit 1
                fi
                sleep 10
        done
else
        echo "Expecting a valid kubernetes namespace"
        exit 1
fi
