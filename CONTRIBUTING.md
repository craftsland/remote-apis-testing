# Contributing

Some guidelines for people wanting to contribute. Also please always feel free
to speak to us, we're very friendly :-)

We welcome contributions in the form of bug fixes or additions. The author of any patch is expected 
to take ownership of that code and is to support it for a reasonable time-frame. This means addressing 
any unforeseen side effects and quirks the feature may have introduced.

## Adding new client and server implementations

Client and server implementations must adhere to the following standards to be compatible with
the test suite:

- The remote instance name passed is called `remote-execution`
- The platform property passed to the REAPI server is a single key-value pair `OSFamily=Linux`
- The client connects to the server via a single unauthenticated endpoint called `frontend` at port `8980`
- Client implementations *must* have a docker-compose service name called `client`
- The server implementation *must* contain a docker-compose service called `frontend` that the client connects to, and it
*must* expose a port at `8980` that the client connects to.
- Client and worker implementations *must* have the following build environment
  - It is built using the `ubuntu20.04` base image
  - The `build-essential` and `libyaml-dev` packages are installed.

When constructing tests:

- All client behaviour which allows for fallback to local execution should be disabled.

- The gitlab shared runners used have only a single 1vCPU. Therefore, it is recommended 
not to pick a client build job that is too large. Please see the [README](README.md#client-jobs) 
for examples.

It is recommended:

- To provide distributions of your client/server implementations as images on a 
publicly accessible container registry.
   - If this is not possible, remote-apis-testing has several examples of containers 
being built using multistage docker builds, with a common build environment 
constructed from ubuntu 20.04

## Patch submissions

Branches must be submitted as merge requests on GitLab: approval is required for
merging onto master (we use Gitlab's 'approval' feature for this) so please seek 
a review from another project member. Asking on slack is probably the best way 
to go about this. 

Some good practice for patch submission:

- Merge requests that are not yet ready for review should be prefixed with the
  ``WIP:`` identifier.
- Submitted branches should not contain a history of work done.

### Commit messages

Commit messages must be formatted with a brief summary line, optionally followed
by an empty line and then a free form detailed description of the change. The
summary line must start with what changed, followed by a colon and a very brief
description of the change.

If the commit is a non functional documentation change e.g. a change to `README.md`, please include [ci skip] in the commit message as referenced [here](https://docs.gitlab.com/ee/ci/yaml/#skipping-jobs))

For some good tips, please see [The seven rules of a great Git commit message](https://chris.beams.io/posts/git-commit/#seven-rules)

## Commit access

We'll give merge rights to anyone who's landed a patch - just ask us on slack to 
amend Gitlab permissions. We don't have a policy for bad actors, and don't expect
to need to have one :) 

