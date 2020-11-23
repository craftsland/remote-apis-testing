"""Utility functions for updating various kinds of references for the
Remote-APIs-Testing repository"""

import subprocess
import re
import requests

# pylint: disable=W0613
# ===== Git commit Hashes =====
def get_latest_commit_hash_from_git_repo(repo, ref, **kwargs):
    """Gets the commit hash for a particular reference on a git repository.
    For instance, if ref = "master", retrieves the latest commit on master."""
    ref_line = subprocess.check_output(["git", "ls-remote", repo, ref], text=True)
    # ref_line will be of the format "{commit_hash}\t{ref}"
    return ref_line.split("\t")[0]


def get_short_latest_commit_hash_from_git_repo(repo, ref, **kwargs):
    """Gets the first 8 characters of the commit hash for a particular reference on
    a git repository"""
    return get_latest_commit_hash_from_git_repo(repo, ref)[:8]


# ===== Git tags ==============
def get_tag_list_from_git_repo(repo, **kwargs):
    """Gets the list of all tags from a specified Git repository"""
    ls_remote_output = subprocess.check_output(["git", "ls-remote", repo], text=True)
    refs_list = ls_remote_output.split("\n")
    tags_list = [
        ref_str.split("\trefs/tags/")[1]
        for ref_str in refs_list
        if "\trefs/tags/" in ref_str
    ]
    return tags_list


def get_highest_version_number_tag_from_git_repo(
    repo, format_string=r"{}.{}.{}", **kwargs
):
    r"""Returns the highest version number tag from a git repo, where a version number
    tag is a tag in the form "\d+.\d+.\d+" eg 5.4.3. Other tags are ignored.
    "10.2.5" is recognized as higher than "9.2.5"."""
    tags_list = get_tag_list_from_git_repo(repo)

    match_string = format_string.format(r"(\d+)", r"(\d+)", r"(\d+)")
    version_number_tag_list = []
    for tag in tags_list:
        match = re.fullmatch(match_string, tag)
        if match:
            vsn_number = [int(match.group(1)), int(match.group(2)), int(match.group(3))]
            version_number_tag_list.append((vsn_number, tag))
    max_tag_tuple = max(version_number_tag_list)
    return max_tag_tuple[1]


def get_short_hash_for_highest_tag_in_git_repo(
    repo, format_string=r"{}.{}.{}", **kwargs
):
    """Finds the highest version number tag for a git repo, then finds the
    commit sha for that tag, and returns the first 8 characters of the sha."""
    tag = get_highest_version_number_tag_from_git_repo(repo, format_string)
    return get_short_latest_commit_hash_from_git_repo(repo, tag)


# ===== Docker tags ===========
def get_tag_list_from_docker_hub(repo, **kwargs):
    """Retrieves the list of tags from a docker repository on Docker Hub."""
    docker_token_url = "https://auth.docker.io/token"
    docker_token_url += "?service=registry.docker.io&scope=repository:{}:pull"

    def get_token_from_docker_hub(repo, **kwargs):
        response = requests.get(docker_token_url.format(repo))
        return response.json()["token"]

    token = get_token_from_docker_hub(repo)
    headers = {
        "Accept": "application/vnd.docker.distribution.manifest.v2+json",
        "Authorization": f"Bearer {token}",
    }
    docker_tags_url = "https://registry-1.docker.io/v2/{}/tags/list"
    response = requests.get(docker_tags_url.format(repo), headers=headers)
    return response.json()["tags"]


def get_max_tag_from_docker_hub(match_prefix, **kwargs):
    """Retrieves the highest tag (in terms of alphabetical sorting) from a docker
    repository on Docker Hub."""
    # BuildBarn repo tags names start with a timestamp in YYYYMMDDTHHMM format,
    # so the latest tag can be found just by sorting alphabetically.
    repo = match_prefix.rstrip(":")
    return max(get_tag_list_from_docker_hub(repo))


# ===== Remote file content ===============
def get_remote_file_content(file_url, **kwargs):
    """Gets the contents of a remote file.
    Will throw an error if the remote file can't be downloaded,
    or if the file content can't be decoded by bytes.decode()"""
    return requests.get(file_url).content.decode()


# ===== Buildfarm Bazel Version ===============
def get_buildfarm_bazel_version(repo, url_string, **kwargs):
    """Retrieves the appropriate Bazel version tag, for the latest Buildfarm tag"""
    tag = get_highest_version_number_tag_from_git_repo(repo)
    file_url = url_string.format(tag)
    return get_remote_file_content(file_url)


# ===== GitLab Container Repo Tags  ===========
# Delete this? Not being used for anything since I found out that BuildGrid docker tags
# were based on BuildGrid git commit hashes, and they were easier to get.
GITLAB_TAGS_URL = "https://gitlab.com/api/v4/projects/{}/registry/repositories/{}/tags"


def get_latest_tag_from_gitlab_container_repo(project_no, repo, **kwargs):
    """Gets the most-recently updated tag from a GitLab container repo.
    Very inneficient, as it involves making an API call for every tag in the repository.
    There ought to be a better way to do this."""

    tags_url = GITLAB_TAGS_URL.format(project_no, repo)
    tag_names_list = []
    next_page = "1"
    while next_page:
        print("Getting list of image tags from GitLab", flush=True)
        paged_url = tags_url + "?page=" + next_page + "&per_page=100"
        response = requests.get(paged_url)
        tag_names_list += [tag["name"] for tag in response.json()]
        next_page = response.headers["X-Next-Page"]
    tag_names_list.remove("latest")
    tags = []
    print(f"{len(tag_names_list, flush=True)} tags found.")
    for tag_name in tag_names_list:
        print(f"Getting metadata for tag {tag_name} from GitLab", flush=True)
        single_tag_url = f"{tags_url}/{tag_name}"
        tag_response = requests.get(single_tag_url)
        tags.append(tag_response.json())

    latest_tag = max(tags, key=lambda tag: tag["created_at"])
    return latest_tag["name"]
