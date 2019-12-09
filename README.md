# Remote Execution API Test Suite

This project provides a test suite designed to be an automated and independent 'acid test' for the [Remote Execution API](https://github.com/bazelbuild/remote-apis) clients and server implementations. You can find us in #remote-apis-testing on [BuildTeam Slack](https://join.slack.com/t/buildteamworld/shared_invite/enQtMzkxNzE0MDMyMDY1LTJiMDg4OWI4MWEwMDAxNGEyYjA3Zjk5ZDQwN2MwNWVkM2NlZTIxOWYxNGJmYTAzYmFlMWUwYjhmNWFkZGU0YTQ), feel free to come and chat, we're very friendly :)

The initial goal of the project was to produce a compatibility matrix showing the status of which RE-API compliant projects worked with which others. We began by building the [Abseil](https://github.com/abseil) library, with the latest version of [Bazel](https://github.com/bazelbuild/bazel), against the latest versions of [Buildbarn](https://github.com/buildbarn), [Buildfarm](https://github.com/bazelbuild/bazel-buildfarm) and [BuildGrid](https://gitlab.com/BuildGrid/buildgrid). We've since added [BuildStream](https://gitlab.com/BuildStream/buildstream) and [RECC](https://gitlab.com/bloomberg/recc), and would like to add more - if you know of another build tool we could add to the tests, please let us know ! 

This initial target was achieved using [Gitlab's CI pipelines](https://docs.gitlab.com/ee/ci/pipelines.html), [Terraform](https://www.terraform.io/) and [Kubernetes](https://kubernetes.io/) with [AWS](https://aws.amazon.com/). The pipelines run once a week on Saturdays and also every time a branch is merged to master (this will happen via an approved merge request). After this, we started to capture performance metrics: end-to-end build times, CPU and memory usage. See the [metrics](https://gitlab.com/remote-apis-testing/remote-apis-testing/wikis/Metrics) page on the wiki. For full details of the pipelines, please see this [blog post](https://www.codethink.co.uk/articles/2019/testing-bazels-remote-execution-api/).

We welcome all contributions, please see our [contributing guide](CONTRIBUTING.md), and to check out what our future plans are, please see the project [Roadmap](https://gitlab.com/remote-apis-testing/remote-apis-testing/wikis/roadmap). 


### Compatibility Matrix

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


### Basic Performance Testing

This shows a build of Bazel(project) with Bazel(client) to produce end-to-end build times.

|                                                       | CAS       | No. Workers | Concurrency per worker | Incremental? |
|-------------------------------------------------------|-----------|-------------|------------------------|--------------|
| ![][bazel-buildgrid-time]                             | In memory | 1           | 1                      |
| ![][bazel-buildgrid-time-incremental]                 | In memory | 1           | 1                      | Yes
| ![][bazel-buildfarm-time-no-concurrency]              | In memory | 1           | 1                      |
| ![][bazel-buildfarm-time-no-concurrency-incremental]  | In memory | 1           | 1                      | Yes
| ![][bazel-buildfarm-time]                             | In memory | 1           | 4                      |
| ![][bazel-buildfarm-time-incremental]                 | In memory | 1           | 4                      | Yes
| ![][bazel-buildbarn-time-no-concurrency]              | In memory | 1           | 1                      |
| ![][bazel-buildbarn-time-no-concurrency-incremental]  | In memory | 1           | 1                      | Yes
| ![][bazel-buildbarn-time]                             | In memory | 1           | 4                      |
| ![][bazel-buildbarn-time-incremental]                 | In memory | 1           | 4                      | Yes

[bazel-buildgrid-time]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildgrid-time.svg
[bazel-buildgrid-time-incremental]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildgrid_incremental-time.svg
[bazel-buildfarm-time]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildfarm-time.svg
[bazel-buildbarn-time]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildbarn-time.svg
[bazel-buildfarm-time-no-concurrency]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildfarm_concurrency_1-time.svg
[bazel-buildbarn-time-no-concurrency]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildbarn_concurrency_1-time.svg
[bazel-buildbarn-time-incremental]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildbarn_incremental-time.svg
[bazel-buildbarn-time-no-concurrency-incremental]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildbarn_concurrency_1_incremental-time.svg
[bazel-buildfarm-time-incremental]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildfarm_incremental-time.svg
[bazel-buildfarm-time-no-concurrency-incremental]: https://remote-apis-testing.gitlab.io/remote-apis-testing/buildfarm_concurrency_1_incremental-time.svg

### Granular Performance Metrics

Please see the [metrics](https://gitlab.com/remote-apis-testing/remote-apis-testing/wikis/Metrics) page on the wiki.

### Documentation

You can find more documentation under the [docs](docs/) folder
