#!/bin/bash

if [ "$#" -ne 2 ]
then
        echo "Expecting two parameters <path-to-trace-folder> <path-to-jaeger-configuration-folder>"
        exit 1
else
        kubectl create namespace jaeger

        kubectl create -f "$2"/jaeger-configuration.yaml

        kubectl create -f "$2"/jaeger-cassandra.yaml

        until kubectl -n jaeger get pods --field-selector=status.phase==Succeeded 2>&1 | grep -q "jaeger-cassandra-schema-job"; do kubectl -n jaeger get pods; sleep 10; done

        kubectl -n jaeger delete job jaeger-cassandra-schema-job

        kubectl create -f "$2"/jaeger-query.yaml

        until kubectl -n jaeger get pods --field-selector=status.phase!=Running 2>&1 | grep -q "No resources found."; do kubectl -n jaeger get pods; sleep 10; done


        cd "$1"

        TABLE_NAMES=$(kubectl exec -n jaeger svc/cassandra -- cqlsh -e "select table_name from system_schema.tables where keyspace_name = 'jaeger_v1_dc1'" | grep -v -E 'table_name|-|\(|^$' | sed "s/^\s*//")

        for TABLE in $TABLE_NAMES
        do
                echo "Copying $TABLE table"
                kubectl exec -n jaeger svc/cassandra -i -- cqlsh -e "copy jaeger_v1_dc1.$TABLE from STDIN with NULL='<null>'" < ${TABLE}.csv
        done
fi
