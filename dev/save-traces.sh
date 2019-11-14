#!/bin/bash

TABLE_NAMES=$(kubectl exec -n jaeger svc/cassandra -- cqlsh -e "select table_name from system_schema.tables where keyspace_name = 'jaeger_v1_dc1'" | grep -v -E 'table_name|-|\(|^$' | sed "s/^\s*//")

mkdir traces

for TABLE in $TABLE_NAMES
do
        echo "Copying $TABLE table to $TABLE.csv"
        kubectl exec -n jaeger svc/cassandra -- cqlsh -e "copy jaeger_v1_dc1.$TABLE to STDOUT with NULL='<null>'" > traces/${TABLE}.csv

        echo "Truncating $TABLE table"
        #kubectl exec -n jaeger svc/cassandra -i -- cqlsh -e "truncate jaeger_v1_dc1.$TABLE" < traces/${TABLE}.csv
done
