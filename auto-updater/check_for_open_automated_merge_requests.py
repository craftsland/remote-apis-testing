#! /usr/bin/env python3
"""
Uses the GitLab API to get a list of open merge requests on the repository,
then confirms that there aren't any pre-existing automated merge requests that are
still open. If there are pre-existing open automated merge request, then the script
exits with sys.exit(1), shutting down the CI process. This avoids producing endless
duplicate Merge Requests.
"""

import argparse
import json
import sys
import requests
from create_merge_request import MR_TITLE_START_TEXT


def main():
    """
    Uses the GitLab API to get a list of open merge requests on the repository,
    then confirms that there aren't any pre-existing automated merge requests that are
    still open. If there are pre-existing open automated merge request, then the script
    exits with sys.exit(1), shutting down the CI process. This avoids producing endless
    duplicate Merge Requests.
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("project_id", help="GitLab project ID")
    arg_parser.add_argument("api_url", help="GitLab's CI API URL")
    args = arg_parser.parse_args()

    api_url = (
        f"{args.api_url}/projects/{args.project_id}/merge_requests"
        + "?state=opened&per_page=100&page={}"
    )
    next_page = 1

    print("Checking for existing automated merge requests.", flush=True)
    while next_page:
        response = requests.get(api_url.format(next_page))
        for merge_request in json.loads(response.content):
            if merge_request["title"].startswith(MR_TITLE_START_TEXT):
                print(
                    "Existing automated merge request found."
                    f"\n\tID: {merge_request['iid']}\t Title: {merge_request['title']}"
                    f"\n\tURL: {merge_request['web_url']}"
                    "\nWill not create a new automated merge request when"
                    " there is an existing request already open."
                    "\nAborting CI job.",
                    flush=True,
                )
                sys.exit(1)
        next_page = response.headers["X-Next-Page"]
    print("None found.\n", flush=True)


if __name__ == "__main__":
    main()
