#!/bin/bash

kubectl apply -f kubernetes/monitoring/namespace.yaml

# Get Fluent-bit definitions
curl https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/fluent-bit-service-account.yaml \
        | sed s/logging/monitoring/ \
        | kubectl apply -f -
curl https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/fluent-bit-role-binding.yaml \
        | sed s/logging/monitoring/ \
        | kubectl apply -f -
kubectl apply -f https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/fluent-bit-role.yaml

# Get Elasticsearch definitions
kubectl apply -f https://download.elastic.co/downloads/eck/1.0.0-beta1/all-in-one.yaml

# Create Elasticsearch Database and Fluent-bit ConfigMap - DaemonSet
kubectl apply -f kubernetes/monitoring/elasticsearch.yaml
kubectl apply -f kubernetes/monitoring/fluent-bit-config.yaml
kubectl apply -f kubernetes/monitoring/fluent-bit-daemonset.yaml
