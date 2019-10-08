# Remote Execution API Test Suite

This project provides a test suite designed to be an automated and independent 'acid test' for the [Remote Execution API](https://github.com/bazelbuild/remote-apis) clients and server implementations. You can find us in #remote-apis-testing on [BuildTeam Slack](https://join.slack.com/t/buildteamworld/shared_invite/enQtMzkxNzE0MDMyMDY1LTJiMDg4OWI4MWEwMDAxNGEyYjA3Zjk5ZDQwN2MwNWVkM2NlZTIxOWYxNGJmYTAzYmFlMWUwYjhmNWFkZGU0YTQ), feel free to come and chat: please use this [invite link](http://tiny.cc/tihy5y) to join our channel. 

The initial goal of the project was to produce a compatibility matrix which showed the status of which projects worked with which others. We began by building the [Abseil](https://github.com/abseil) library, with the latest version of [Bazel](https://github.com/bazelbuild/bazel), against the latest versions of Buildbarn, Buildfarm and BuildGrid. We've since added [BuildStream](https://gitlab.com/BuildStream/buildstream) and [RECC](https://gitlab.com/bloomberg/recc), and would like to add more - if you know of another build tool we could add to the tests, please let us know ! 

This initial target was achieved using Gitlab CI, Terraform and Kubernetes with AWS. The pipelines run once a week on Saturdays and also every time a branch is merged to master (this will happen via an approved merge request). After this, we started to capture performance metrics: end-to-end build times, CPU and memory usage. See the [metrics](https://gitlab.com/remote-apis-testing/remote-apis-testing/wikis/Metrics) page on the wiki.

We welcome all contributions, please see our [contributing guide](CONTRIBUTING.md), and to check out what our future plans are, please see the project [Roadmap](https://gitlab.com/remote-apis-testing/remote-apis-testing/wikis/roadmap). 


#### Compatibility Matrix

This shows the status of client implementations against server implementations in a set of tests.

|             | BuildGrid                  | Buildfarm            | Buildbarn            |
|-------------|----------------------------|----------------------|----------------------|
| Bazel       | ![][bazel-buildgrid]       | ![][bazel-buildfarm] | ![][bazel-buildbarn] |
| BuildStream | ![][buildstream-buildgrid] | Not compatible       | Not compatible       |
| RECC        | ![][recc-buildgrid]        | TBA                  | TBA                  |
| Goma        | TBA                        | TBA                  | TBA                  |

[bazel-buildgrid]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildgrid-bazel-deployed.svg
[bazel-buildfarm]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildfarm-bazel-deployed.svg
[bazel-buildbarn]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildbarn-bazel-deployed.svg
[buildstream-buildgrid]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildgrid-buildstream-deployed.svg
[recc-buildgrid]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildgrid-recc-deployed.svg


#### Basic Performance Testing

This shows a build of Bazel(project) with Bazel(client) to produce end-to-end build times.

|                                          | CAS       | No. Workers | Concurrency per worker |
|------------------------------------------|-----------|-------------|------------------------|
| ![][bazel-buildgrid-time]                | In memory | 1           | 1                      |
| ![][bazel-buildfarm-time-no-concurrency] | In memory | 1           | 1                      |
| ![][bazel-buildfarm-time]                | In memory | 1           | 4                      |
| ![][bazel-buildbarn-time-no-concurrency] | In memory | 1           | 1                      |
| ![][bazel-buildbarn-time]                | In memory | 1           | 4                      |

[bazel-buildgrid-time]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildgrid-time.svg
[bazel-buildfarm-time]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildfarm-time.svg
[bazel-buildbarn-time]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildbarn-time.svg
[bazel-buildfarm-time-no-concurrency]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildfarm-concurrency-1-time.svg
[bazel-buildbarn-time-no-concurrency]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildbarn-concurrency-1-time.svg

#### Granular Performance Metrics

Please see the [metrics](https://gitlab.com/remote-apis-testing/remote-apis-testing/wikis/Metrics) page on the wiki.


## Pipeline Set-up

#### Terraform

Terraform deployments can be found in the `terraform/` folder.

To provision the desired cluster, go to the corresponding folder and first initialise terraform with:

```
$ terraform init
```
You need to configure your AWS credentials to be in environment variables as explained [here](https://www.terraform.io/docs/providers/aws/#environment-variables):

```
$ export AWS_ACCESS_KEY_ID="anaccesskey"
$ export AWS_SECRET_ACCESS_KEY="asecretkey"
```
Then execute the following to actually provision the cluster infrastructure:

```
$ terraform apply
```

You can find variables available to edit in  `terrform/variables.tf`.

To change these variables in the command line, use the -var option (see [here](https://aws.amazon.com/ec2/instance-types/) for instance specs):

```
$ terraform apply -var cluster_name=foo
```

When you are done with your testing, you can destroy the cluster with:

```
$ terraform destroy
```

### Kubernetes

Kubernetes deployments can be found in the Kubernetes folder. They are
created with the following command:

```
kubectl create -f kubernetes/<deployment>/
```

You can check on the status of your cluster with:

```
kubectl get all --all-namespaces
```

Clients are run as a job in the cluster and can be found in
`kubernetes/jobs/` folder.

To see the logs of a job, you can use for example:

```
kubectl logs jobs/abseil -n buildbarn
```

## Local Testing

### kind

[kind](https://github.com/kubernetes-sigs/kind) allows us to spin up a kubernetes cluster in docker which we can deploy our services to.
This allows you to test various `kubernetes/` configurations without the need for a cloud provider. You can start up a cluster with:

```
kind create cluster
```

Once the cluster is up and running, you can spin up the individual services in `kubernetes/`:

```
# Spin up the server side services
$ kubectl kustomize kubernetes/server/overlays/<server>/<client>/ | kubectl create -f -

# Spin up a client job
$ kubectl create -f kubernetes/client/<client>/<server>/<job>.yml

# See the running pods with
$ kubectl get pod -n <server>

# View the logs with
$ kubectl logs --follow -n <server> <POD NAME>
```


### Minikube

You can test changes to the Kubernetes deployments locally (avoiding the
need for a cloud provider) with [minikube](https://github.com/kubernetes/minikube).
Note that you'll need at least 4GB of RAM available to your cluster,
which can be achieved with the following command:

```
minikube start --vm-driver kvm2 --memory 4096
```

### dind-cluster

You can also test locally with a multi-node setup using the pre configured [dind-cluster](https://github.com/kubernetes-retired/kubeadm-dind-cluster#using-preconfigured-scripts) script.

```
./dind-cluster.sh up
```

As dind-cluster does not include a storage provisioner, you need to deploy one manually. This can be done using a helper script available in `./dev/`.

```
chmod +x ./dev/storage_setup.sh
./dev/storage_setup.sh up
```

Assuming you already have `kubectl` installed, these commands will also
configure it to use your minikube/dind cluster. After this you can use `kubectl`
commands as described above against your cluster to test your changes as
needed.
