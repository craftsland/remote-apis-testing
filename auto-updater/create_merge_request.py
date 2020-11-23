#!/usr/bin/env python3
"""
Pushes the local commits to GitLab as a new branch, then creates a Merge Request to
merge into master.
"""

import argparse
import datetime
import json
import subprocess
import sys
import requests

DESCRIBE_TEXT = """
Pushes the local commits to GitLab as a new branch, then creates a Merge Request to
merge into master.
"""


def main():
    """See main module docstring."""
    # Get args
    arg_parser = argparse.ArgumentParser(description=DESCRIBE_TEXT)
    arg_parser.add_argument("project_id", help="GitLab project ID")
    arg_parser.add_argument("api_url", help="GitLab's CI API URL")
    arg_parser.add_argument(
        "token_file", help="File containing a GitLab API access token,"
    )
    args = arg_parser.parse_args()

    # Create Branch
    new_branch = f"auto-update/{datetime.date.today()}"
    subprocess.run(["git", "checkout", "-b", new_branch], check=True)
    # Push Branch
    print("Pushing new branch to remote repo.", flush=True)
    subprocess.run(["git", "push", "origin", new_branch], check=True)

    # Get access token
    with open(args.token_file, mode="r") as token_file:
        api_token = token_file.read().strip()

    # Create MR
    print("Creating new Merge Request.", flush=True)
    api_merge_request_url = f"{args.api_url}/projects/{args.project_id}/merge_requests"
    headers = {"PRIVATE-TOKEN": f"{api_token}"}
    data = {
        "id": args.project_id,
        "source_branch": new_branch,
        "target_branch": "master",
        "remove_source_branch": True,
        "title": f"Automated update {datetime.date.today()}",
    }
    response = requests.post(api_merge_request_url, data=data, headers=headers)
    print(
        f"\tAPI call status code: {response.status_code}"
        f"\n\tAPI call reason: {response.reason}"
    )
    if response.status_code != 201:
        sys.exit(1)
    content = json.loads(response.content)
    print("Merge Request Created:", flush=True)
    print(f"\tIID: {content['iid']}, Title:{content['title']}", flush=True)
    print(f"\tURL: {content['web_url']}", flush=True)


if __name__ == "__main__":
    main()
