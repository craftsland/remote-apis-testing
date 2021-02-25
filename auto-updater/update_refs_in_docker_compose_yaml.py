#!/usr/bin/env python3
"""Identifies various references in the docker-compose yaml files, (docker tags,
git commit hashes, etc.) and updates them to the most recent versions. Commits the
updates to each file as a new Git commit."""

from collections import namedtuple
from update_refs_in_file import update_refs_in_file_and_commit_changes
from get_up_to_date_references import (
    get_highest_version_number_tag_from_git_repo,
    get_max_tag_from_docker_hub,
    get_latest_commit_hash_from_git_repo,
    get_buildfarm_bazel_version,
    get_short_hash_for_highest_tag_in_git_repo,
)

FileData = namedtuple("FileData", ["name", "filename", "refs"])

FILELIST = [
    FileData(
        name="Buildbarn",
        filename="../docker-compose/docker-compose-buildbarn.yml",
        refs=[
            {
                "function": get_max_tag_from_docker_hub,
                "match_prefix": "buildbarn/bb-storage:",
            },
            {
                "function": get_max_tag_from_docker_hub,
                "match_prefix": "buildbarn/bb-scheduler:",
            },
            {
                "function": get_max_tag_from_docker_hub,
                "match_prefix": "buildbarn/bb-browser:",
            },
            {
                "function": get_max_tag_from_docker_hub,
                "match_prefix": "buildbarn/bb-worker:",
            },
            {
                "function": get_max_tag_from_docker_hub,
                "match_prefix": "buildbarn/bb-runner-installer:",
            },
        ],
    ),
    FileData(
        name="Buildfarm",
        filename="../docker-compose/docker-compose-buildfarm.yml",
        refs=[
            {
                "function": get_highest_version_number_tag_from_git_repo,
                "match_prefix": "BUILDFARM_VERSION:",
                "repo": "https://github.com/bazelbuild/bazel-buildfarm.git",
            },
            {
                "function": get_buildfarm_bazel_version,
                "display_name": "Buildfarm Bazel version",
                "match_prefix": "BAZEL_VERSION:",
                "repo": "https://github.com/bazelbuild/bazel-buildfarm.git",
                "url_string": "https://raw.githubusercontent.com/bazelbuild/"
                + "bazel-buildfarm/{}/.bazelversion",
            },
        ],
    ),
    FileData(
        name="Buildgrid",
        filename="../docker-compose/docker-compose-buildgrid.yml",
        refs=[
            {
                "function": get_highest_version_number_tag_from_git_repo,
                "display_name": "latest BuildGrid tag",
                "match_prefix": "registry.gitlab.com/buildgrid/buildgrid/buildgrid:[^ ]* #",
                "repo": "https://gitlab.com/BuildGrid/buildgrid.git",
            },
            {
                "function": get_short_hash_for_highest_tag_in_git_repo,
                "display_name": "latest BuildGrid tag (short commit hash)",
                "match_prefix": "registry.gitlab.com/buildgrid/buildgrid/buildgrid:",
                "repo": "https://gitlab.com/BuildGrid/buildgrid.git",
            },            {
                "function": get_highest_version_number_tag_from_git_repo,
                "match_prefix": "BUILDBOX_COMMON_VERSION:",
                "repo": "https://gitlab.com/BuildGrid/buildbox/buildbox-common.git",
            },
            {
                "function": get_highest_version_number_tag_from_git_repo,
                "match_prefix": "BUILDBOX_WORKER_VERSION:",
                "repo": "https://gitlab.com/BuildGrid/buildbox/buildbox-worker.git",
            },

        ],
    ),
    FileData(
        name="Bazel",
        filename="../docker-compose/docker-compose-bazel.yml",
        refs=[
            {
                "function": get_highest_version_number_tag_from_git_repo,
                "match_prefix": "BAZEL_VERSION:",
                "repo": "https://github.com/bazelbuild/bazel.git",
            },
        ],
    ),
    FileData(
        name="Remote_asset",
        filename="../docker-compose/docker-compose-remote_asset.yml",
        refs=[
            {
                "function": get_max_tag_from_docker_hub,
                "match_prefix": "buildbarn/bb-remote-asset:",
            }
        ],
    ),
    FileData(
        name="Goma",
        filename="../docker-compose/docker-compose-goma.yml",
        refs=[
            {
                "function": get_latest_commit_hash_from_git_repo,
                "match_prefix": "GOMA_CLIENT_GIT_SHA:",
                "repo": "https://chromium.googlesource.com/infra/goma/client.git",
                "ref": "master",
            },
            {
                "function": get_highest_version_number_tag_from_git_repo,
                "match_prefix": "GOMA_SERVER_VERSION:",
                "repo": "https://chromium.googlesource.com/infra/goma/server",
                "format_string": r"v{}\.{}\.{}",
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
                "match_prefix": "PANTS_COMMIT:",
                "repo": "https://github.com/pantsbuild/example-python.git",
                "ref": "main",
            },
        ],
    ),
    FileData(
        name="RECC",
        filename="../docker-compose/docker-compose-recc.yml",
        refs=[
            {
                "function": get_highest_version_number_tag_from_git_repo,
                "match_prefix": "RECC_VERSION:",
                "repo": "https://gitlab.com/bloomberg/recc.git",
            },
            {
                "function": get_highest_version_number_tag_from_git_repo,
                "match_prefix": "BUILDBOX_COMMON_VERSION:",
                "repo": "https://gitlab.com/BuildGrid/buildbox/buildbox-common.git",
            },
            {
                "function": get_highest_version_number_tag_from_git_repo,
                "match_prefix": "BUILDBOX_WORKER_VERSION:",
                "repo": "https://gitlab.com/BuildGrid/buildbox/buildbox-worker.git",
            },

        ],
    ),
]


def main():
    """Main function, see module docstring"""
    print("Searching for available updates:", flush=True)
    for file_data in FILELIST:
        update_refs_in_file_and_commit_changes(file_data)


if __name__ == "__main__":
    main()
