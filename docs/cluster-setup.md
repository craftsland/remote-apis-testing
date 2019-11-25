# Cluster setup

> Before starting a cluster you need a test environment up and running either locally or in AWS.  
> You can leanr how to do this in the [Environment setup][environment setup] section.

The different kubernetes configuration files are all located under `kubernetes/`  
They are sepearated in three groups:

+ [server](#Server)

+ [client](#Client)

+ [monitoring](#Monitoring)

  + [jaeger](#Jaeger)

## Server

This section is defining the Remote Execution implementation side. Currently there are configuration for [Buildfarm][buildfarm], [Buildbarn][buildbarn] and [Buildgrid][buildgrid].

To create the services required use:
```
# Spin up the server side services
$ kubectl kustomize kubernetes/server/overlays/<server>/<client>/ | kubectl create -f -
```

You can then monitor the status of the cluster with:
```
# To get the current pods status of the server implementation you chose
kubectl -n <server> get pods

# To keep watching the pods status of server implementation you chose
kubectl -n <server> get pods -w
```

## Client

The client represents the tools which will interact with the Remote Execution implementation. This project is configured to use either [Bazel][bazel], [Buildstream][buildstream], [Recc][recc].
> You can find which client works with which server in the [Compatibility Matrix][compatibility matrix] section of the README.

Once all the pods in the server side are running you can create the kubernetes job to start a build using:

```
# Spin up a client job
$ kubectl create -f kubernetes/client/<client>/<server>/<job>.yml

# View the logs with
$ kubectl -n <server> logs --follow job/<job>

```

## Monitoring

### Jaeger

To Do

[environment setup]: environment-setup.md
[buildfarm]: https://github.com/bazelbuild/bazel-buildfarm
[buildbarn]: https://github.com/buildbarn
[buildgrid]: https://gitlab.com/BuildGrid/buildgrid
[bazel]: https://bazel.build/
[buildstream]: https://buildstream.build/
[recc]: https://gitlab.com/bloomberg/recc
[compatibility matrix]: ../README.md#compatibility-matrix
