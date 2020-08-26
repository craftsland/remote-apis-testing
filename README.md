# Remote Execution API Test Suite

This project provides a test suite designed to be an automated and independent 'acid test' for the [Remote Execution API](https://github.com/bazelbuild/remote-apis) clients and server implementations. You can find us in #remote-apis-testing on [BuildTeam Slack](https://join.slack.com/t/buildteamworld/shared_invite/enQtMzkxNzE0MDMyMDY1LTJiMDg4OWI4MWEwMDAxNGEyYjA3Zjk5ZDQwN2MwNWVkM2NlZTIxOWYxNGJmYTAzYmFlMWUwYjhmNWFkZGU0YTQ), feel free to come and chat, we're very friendly :)

We provide a set of docker-compose deployments for client and server implementations. These will run readily on your local machine or on CI. Therefore, these deployments
are also useful for trying out new clients or servers in the REAPI ecosystem, although we must warn that NONE of these are production ready!

We welcome all contributions, please see our [contributing guide](CONTRIBUTING.md)

### Compatibility Matrix

This shows the status of client implementations against server implementations.

Clients will run a short build task against server implementations. If the client job is successful, then this is
denoted as a success. Otherwise, the job is marked as a failure.

If you would like to add a new client or server on to this list, you can find instructions at [CONTRIBUTING.md](CONTRIBUTING.md#adding-new-client-and-server-implementations)

#### Client jobs

- Bazel: Building [abseil-hello](https://github.com/abseil/abseil-hello/tree/master/bazel-hello)
- Goma & Recc: Building [libcyaml](https://github.com/tlsa/libcyaml)

|                   | BuildGrid                      | Buildfarm                      | Buildbarn                      |
| ----------------- | ------------------------------ | ------------------------------ | ------------------------------ |
| Bazel             | ![][bazel-buildgrid]           | ![][bazel-buildfarm]           | ![][bazel-buildbarn]           |
| Bazel + asset-hub | ![][bazel-buildgrid-asset-hub] | ![][bazel-buildfarm-asset-hub] | ![][bazel-buildbarn-asset-hub] |
| BuildStream       | TBA                            | TBA                            | TBA                            |
| RECC              | ![][recc-buildgrid]            | ![][recc-buildfarm]            | ![][recc-buildbarn]            |
| Goma              | ![][goma-buildgrid]            | ![][goma-buildfarm]            | ![][goma-buildbarn]            |
| Pants             | TBA                            | TBA                            | TBA                            |
| Please            | TBA                            | TBA                            | TBA                            |

[bazel-buildgrid]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildgrid-bazel-deployed.svg
[bazel-buildgrid-asset-hub]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildgrid-bazel-asset-hub-deployed.svg
[bazel-buildfarm]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildfarm-bazel-deployed.svg
[bazel-buildfarm-asset-hub]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildfarm-bazel-asset-hub-deployed.svg
[bazel-buildbarn]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildbarn-bazel-deployed.svg
[bazel-buildbarn-asset-hub]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildbarn-bazel-asset-hub-deployed.svg
[recc-buildgrid]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildgrid-recc-deployed.svg
[recc-buildfarm]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildfarm-recc-deployed.svg
[recc-buildbarn]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildbarn-recc-deployed.svg
[goma-buildgrid]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildgrid-goma-deployed.svg
[goma-buildfarm]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildfarm-goma-deployed.svg
[goma-buildbarn]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildbarn-goma-deployed.svg

### Running tests

You will require

- Docker engine (>= 18.09 with Buildkit installed)
- Docker compose (>=1.25.1)

To run:

```
cd docker-compose
./run.sh -s <SERVER_DOCKER_COMPOSE_FILE> -c <CLIENT_DOCKER_COMPOSE_FILE>
```

The exit code for the script will correspond to the return code for the client container.