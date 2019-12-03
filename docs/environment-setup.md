# Environment setup

This documents the steps to follow in order to recreate the test environement to run:

+ [Local](#Local)
  + [Kind](#Kind)

+ [AWS](#AWS)
  + [Terraform](#Terraform)


# Local

## Kind

[Kind][kind] allows us to spin up a kubernetes cluster in docker which we can deploy our services to.
This allows you to test various `kubernetes/` configurations without the need for a cloud provider. You can start up a cluster with:

```
kind create cluster
```

> For versions of Kind prior to 0.6.0 you need to export the kubeconfig using `export KUBECONFIG="$(kind get kubeconfig-path)"`

You can make sure that your cluster is running and properly configured running:

```
kubectl get pods --all-namespaces
```

Once you are finished testing you can stop the cluster with:

```
kind delete cluster
```

# AWS

## Terraform

Terraform deployments can be found in the `terraform/` folder.

To provision the desired cluster, go to the corresponding folder and first initialise terraform with:

```
$ terraform init
```

You need to configure your AWS credentials to be in environment variables as explained [here][terraform env variables]:

```
$ export AWS_ACCESS_KEY_ID="anaccesskey"
$ export AWS_SECRET_ACCESS_KEY="asecretkey"
```

Then execute the following to actually provision the cluster infrastructure:

```
$ terraform apply
```

> Make sure to don't delete the file generated by terraform at this stage otherwise you will not be able to use terraform to destroy  the cluster

You can find variables available to edit in  `terraform/variables.tf`.

To change these variables in the command line, use the -var option (see [here][amazon ec2 instances] for instance specs):

```
$ terraform apply -var cluster_name=foo
```

Before being able to run kubetcl commands you need to export the kubeconfig using:

```
export KUBECONFIG=<path-to-the-project>/terraform/kubeconfig_k8-cluster<cluster-name-you-chose>
```

> It is better to use the absolute path to the project (or relative to your home folder) in order to keep a valid path to the kubeconfig no matter where you are

When you are done with your testing, you can destroy the cluster with:

```
$ terraform destroy
```


[kind]: https://github.com/kubernetes-sigs/kind
[terraform env variables]: https://www.terraform.io/docs/providers/aws/#environment-variables
[amazon ec2 instances]: https://aws.amazon.com/ec2/instance-types/