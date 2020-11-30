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

## Automated ref updates

As part of the CI process, the project runs a regular scheduled job to look for updates
to each client/server. If the script finds new versions of one or more software, it will
automatically create a new branch that includes the update, then generate a merge request
to merge the update into master.

The script works by editing the `docker-compose-{service}.yml` files in the
`/docker-compse` directory. It updates one or more "refs" in each file, where a ref
might be:
* A git commit sha
* A git tag
* A docker repository tag
* Any other identifier that can be found by an automated script

To enable automated updates for a new server or a new client, you need to add a new
namedtuple to the list in `update_refs_in_docker_compose_yaml.py`. For example:

```
    FileData(
        name="Buildbarn",
        filename="../docker-compose/docker-compose-buildbarn.yml",
        refs=[
            {
                "function": get_max_tag_from_docker_hub,
                "match_prefix": "buildbarn/bb-storage:"
            },
            {
                "function": get_max_tag_from_docker_hub,
                "match_prefix": "buildbarn/bb-scheduler:"
            },
        ],
    ),
    FileData(
        name="Pants",
        filename="../docker-compose/docker-compose-pants.yml",
        refs=[
            {
                "function": get_latest_commit_hash_from_git_repo,
                "display_name": "pants commit",
                "match_prefix": "git checkout",
                "repo": "https://github.com/pantsbuild/example-python.git",
                "ref": "main",
            },
        ],
    ),
```

- `filename` is the path to the docker-compose yaml file (relative to the
  `auto-updater` directory).
- `name` is a human-readable name for the client or server represented by that
  file. It is used to print human-readable messages in the updater's output,
  (including in the auto-generated git commits).
- Each `ref` is a dictionary definining one "reference" that exists in the
  docker-compose yaml file, plus the information needed to update that
  reference.  These references might be a git SHA, a docker tag and version
  number, etc. The dictionary must include the keys `match_prefix` and `function`.
- `function` is a function that will retrieve the new ref. Several such
  functions are defined in `get_up_to_date_references.py`, and more can be
  added. For instance, `get_highest_version_number_tag_from_git_repo` accepts a
  repository URL as a keyword argument (keyword `repo`), and returns the highest
  version number that exists amongst that repository's tags.
- The function is invoked by submitting the entire `ref` dictionary as
  \*\*kwargs, so it should accept only keyword arguments. It should also be
  prepared to ignore keyword arguments that it doesn't need.
- `match_prefix` is used to locate the old ref inside the docker-compose yaml
  file, so that it can be replaced with the new ref. It should be a regular
  expression that occurs immediately before the ref. eg the prefix
  `"RECC_VERSION:"` is used for updating the string `"RECC_VERSION: 1.0.1"`.
- Note that when the `function` is invoked it will receive the `match_prefix`
  as a keyword-argument, which it may either use or ignore. For instance,
  `get_max_tag_from_docker_hub` uses `match_prefix` to identify the relevant
  docker image, and doesn't require any other arguments.
- `display_name` is an optional key that will be used to refer to the ref in
  human-readable outputs (including the commit message) eg `pants commit` above.
  If this isn't specified, then `match_prefix` will be used as the display name.
- Other keyword arguments will depend on the function being used.

`update_refs_in_docker_compose_yaml.py` can be run locally, to test that the
auto-update is set up correctly. Try editing the docker file to have an earlier
version of the ref(s), then run the script. The script should restore everything
to the latest version (or to newer versions, if they are available).

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

