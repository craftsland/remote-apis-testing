# Fluent-bit

[Fluent-bit][fluent-bit] is a lightweight log Processor and Forwarder written in C.  
It's purpose is to extract logs from the different elements running in the Kubernetes cluster, structure them as well as enrich them with metadata before forwarding the final result to a central place.

You can find more information about [Fluent-bit][fluent-bit] internals and design in the [officials docs][official-docs]

## Project's Structure

This project uses the recommended configuration for using [Fluent-bit][fluent-bit] in Kubernetes.  
Fluent-bit runs as a DaemonSet reading the logs directly from the Docker log files, formating the logs based on Logstash approach before forwarding the logs to an Elasticsearch database.

## Deploying 

Adding logging aggregation to the Kubernetes cluster run the following script:

```
dev/logging-aggregation-setup.sh
```

This script will add all the required elements to the cluster and create a Fluent-bit DaemonSet and an Elasticsearch database.  
> Currently it will only aggregate the containers logs and will not extract any Bazel or Remote Execution logs

## Visualizing logs using Kibana

In order to view the logs using Kibana first start Kibana server with:

```
kubectl apply -f kubernetes/monitoring/kibana.yaml
```

Once it is started make it available outside your cluster

```
kubectl -n monitoring port-forward service-kibana-kb 5601
```

you can now access Kibana by browsing to `localhost:5601`  
You will be asked to log in the user name is `elastic` to get the password run the following command:

```
echo $(kubectl -n monitoring get secret elasticsearch-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode)
```
Once you have logged in, a basic view of the incoming logs can be seen by first navigating to the settings page, clicking on `index patterns`, and creating a new index pattern from the logstash listed. (When prompted select `@timestamp` from the drop down list). You will then be able to see the logs by clicking on the small compass icon at the top of the list of icons on the left of the page.

[fluent-bit]: https://fluentbit.io/
[official-docs]: https://docs.fluentbit.io/manual/getting_started
