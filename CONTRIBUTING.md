# Contributing

Some guidelines for people wanting to contribute. Also please always feel free
to speak to us, we're very friendly :-)

We welcome contributions in the form of bug fixes or additions. Please note that
developer access is restricted and must be requested due to the cloud resources
used in the CI. See [MAINTAINERS.md](MAINTAINERS.md) for contact information of those who can
assist you in gaining the privileges for your contributions.

The author of any patch is expected to take ownership of that code and is to
support it for a reasonable time-frame. This means addressing any unforeseen
side effects and quirks the feature may have introduced.

## Modifying .gitlab-ci.yml

Modifications to .gitlab-ci.yml are expected to maintain a similar structure
and naming convention across jobs and stages. Clients are generally grouped
into stages building against each server implementation with the exception of
speedtests (building the bazel project) where each speedtest gets its own stage.
This is to prevent multiple jobs running alongside the job and potentially
hindering performance.

Badges are stored in `badges/` until the `pages` job runs (only on master)
and moves the contents to `public/` and making them available via gitlab pages.

## Patch submissions

Branches must be submitted as merge requests on GitLab: approval is required for
merging onto master (we use Gitlab's 'approval' feature for this) so please seek 
a review from another project member. Asking on slack is probably the best way 
to go about this. 

Some good practice for patch submission:

- Merge requests that are not yet ready for review should be prefixed with the
  ``WIP:`` identifier.
- Submitted branches should not contain a history of work done.
- Unit tests should be a separate commit.

Please see [kubernetes/README.md](kubernetes/README.md) for a reference on adding new server/client
implementation kubernetes configurations.

### Commit messages

Commit messages must be formatted with a brief summary line, optionally followed
by an empty line and then a free form detailed description of the change. The
summary line must start with what changed, followed by a colon and a very brief
description of the change.

If the commit is a non functional documentation change e.g. a change to `README.md`, please include [ci skip] in the commit message as referenced [here](https://docs.gitlab.com/ee/ci/yaml/#skipping-jobs))

For some good tips, please see [The seven rules of a great Git commit message](https://chris.beams.io/posts/git-commit/#seven-rules)


## Cloud Resources

The CI pipelines spin up a kubernetes cluster on a cloud platform and therefore come
at a cost. Some qwerks with the pipeline must be considered when working on patches and
triggering pipelines. Most notably, cancelling a pipeline will cancel the cleanup job and
therefore leave the kubernetes cluster running. If this does happen, please check [MAINTAINERS.md](MAINTAINERS.md)
for the contact details of someone who should have administrator access to the cloud services. 

### Maintainer resource cleanup guide

When cleaning up resources which have escaped cleanup through some means, it is crucial to delete several resources. First delete the cluster which can be found on the
`Services -> Compute -> EKS` page. Secondly, navigate to `Services -> Compute -> EC2` and check `Volumes`, `Load Balancers`, `Auto Scaling Groups` and `Security Groups` for resources which are related to the pipelines which have avoided cleanup. If performing a large cleanup of resources, ensure all pipelines are finished and it is 
safe to delete all remaining resources.

## Commit access

We'll give merge rights to anyone who's landed a patch - just ask us on slack to 
amend Gitlab permissions. We don't have a policy for bad actors, and don't expect
to need to have one :) 

## Project Maintainence

It should be noted that the project currently pins the version of bazel used to build job targets,
the version number is set and can be modified within the [.gitlab-ci.yml](.gitlab-ci.yml) `variables:` field. This 
can be updated on release of a new bazel version and merged to master upon success of the build jobs.
