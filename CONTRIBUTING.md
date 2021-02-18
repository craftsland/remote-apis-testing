# Contributing

Some guidelines for people wanting to contribute. Also please always feel free
to speak to us, we're very friendly :-)

We welcome contributions in the form of bug fixes or additions. The author of any patch is expected
to take ownership of that code and is to support it for a reasonable time-frame. This means addressing
any unforeseen side effects and quirks the feature may have introduced.

## Adding new client and server implementations

Client and server implementations must adhere to the following standards to be compatible with
the test suite:

- Client/Server/Asset names **must** not include `-`, instead use `_` to split multiple words.
- The remote instance name passed is called `remote-execution`
- The platform property passed to the REAPI server is a single key-value pair `OSFamily=linux`
- The client connects to the server via a single unauthenticated endpoint called `frontend` at port `8980`
- Client implementations *must* have a docker-compose service name called `client`
- The server implementation *must* contain a docker-compose service called `frontend` that the client connects to, and it
*must* expose a port at `8980` that the client connects to.
- A remote asset server implementation *must* contain a docker-compose service called `asset` that the client connects to, and it
*must* expose a port at `8979` that the client connects to.
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

## `Matrix.yml`, Jinja2 templates, and automated ref updates

For the remote-apis-testing project to be as useful as possible, it's important
to always use the most up to date version of clients, servers, and remote-asset
servers. To make it as easy as possible to keep each implementation up to date,
we use jinja-2 templates, and a central file called `matrix.yml` which stores
version numbers.

To create a jinja2 template file, start by writing a docker-compose yaml file
for your project. Then, identify any elements which will change whenever a new
version of your project is released. `matrix.yml` refers to these as
`version_refs`, and they would be things like version numbers, docker tags, or
git commit hashes. Replace these values with variable names, and enclose the
variable names in `{{double curly braces}}`. Finally, save the file with the
suffix `.jinja2_template` and add the file to the `docker-compose-templates`
directory.

eg from `docker-compose-buildfarm.jinja2_template`:
```
version: '3.4'
services:
  frontend:
    build:
      context: docker
      target: buildfarm
      args:
        BUILDFARM_VERSION: {{BUILDFARM_VERSION}}
        BAZEL_VERSION: {{BUILDFARM_BAZEL_VERSION}} # Version of Bazel required to build Buildfarm
        BUILDFARM_DAEMON: buildfarm-server
        BUILDFARM_CONFIG: /config/server.config
    ports:
...
```

Then, create a new dictionary within the `projects` section of `matrix.yml`.
This dictionary tells the project where to find the template file, and which
values to substitute in for each variable. It should also have information which
will be used by the auto-updater (see below).

eg (from `matrix.yml`):
```
  buildfarm:
    filename: docker-compose-buildfarm.jinja2_template
    version_refs:
      BUILDFARM_VERSION:
        value: 1.6.0
        update_function: get_highest_version_number_tag_from_git_repo
        update_args:
          repo: https://github.com/bazelbuild/bazel-buildfarm.git
      BUILDFARM_BAZEL_VERSION:
        value: 3.6.0
        update_function: get_buildfarm_bazel_version
        update_args:
          repo: https://github.com/bazelbuild/bazel-buildfarm.git
          url_string: https://raw.githubusercontent.com/bazelbuild/bazel-buildfarm/{}/.bazelversion
  buildgrid:
    filename: docker-compose-buildgrid.jinja2_template
...
```

When tests are run, a script will use the template file to generate
docker-compose yaml, by substituting in the relevant value for each variable.

As part of the CI process, GitLab runs a regular scheduled job to look for
updates to each client/server. If the script finds new versions of one or more
software projects, it will automatically update the relevant values in
`matrix.yml`, commit the changes, and create a new merge request.

Specifically, the auto-updater will update each variable individually, by
running the associated `update_function`, with the associated `update_args`
supplied to it as keyword arguments. Update functions are stored in
the python library file `auto-updater/get_up_to_date_references.py`, and new
functions can be added if needed.

Update functions should accept only keyword arguments, and should
return a single string. eg `get_highest_version_number_tag_from_git_repo`
returns a string like `1.6.2`, and this would then be used to overwrite the
existing `1.6.0` value.

If it isn't possible to supply a suitable update function, you can set
`update_function: null` or just `update_function:` (with nothing after the
colon), to tell the auto-updater that it should skip this variable. 

`auto-updater/update_refs_in_docker_compose_yaml.py` can be run locally, to
test that the auto-update is set up correctly. If there are new versions
available, then the script should detect them. If there are no new versions
avialable, try editing refs in `matrix.yml` to earlier versions (and commit that
edit as a temporary commit). Running the script should then restore the current
version.

## Static site

This project generates a static site on CI runs. This is done via [hugo](gohugo.io). 
The `-j` flag is passed to `run.sh` during CI, spitting out json files containing the 
status of the run. These are then merged into a single object and placed into the sites 
`data` folder which the hugo theme uses to generate the markup for the compatability matrix.
The expected format for this is detailed in `site/themes/casper/README.md`.

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

