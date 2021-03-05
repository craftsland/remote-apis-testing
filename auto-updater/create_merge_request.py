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

MR_TITLE_START_TEXT = "Automated update"


def get_args():
    """Parse command line arguments."""
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument("project_id", help="GitLab project ID")
    arg_parser.add_argument("api_url", help="GitLab's CI API URL")
    arg_parser.add_argument(
        "token_file", help="File containing a GitLab API access token,"
    )
    arg_parser.add_argument(
        "--webhook_url_file",
        default=None,
        help=(
            "File conatining a webhook url (eg for a Slack Channel). If given, script"
            " will attempt to send a message to this webhook, creating an alert about"
            " the new MR."
        ),
    )
    args = arg_parser.parse_args()
    return args


def main():
    """See main module docstring."""
    args = get_args()

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
    mr_headers = {"PRIVATE-TOKEN": f"{api_token}"}
    mr_data = {
        "id": args.project_id,
        "source_branch": new_branch,
        "target_branch": "master",
        "remove_source_branch": True,
        "title": f"{MR_TITLE_START_TEXT} {datetime.date.today()}",
    }
    mr_response = requests.post(api_merge_request_url, data=mr_data, headers=mr_headers)
    print(
        f"\tAPI call status code: {mr_response.status_code}"
        f"\n\tAPI call reason: {mr_response.reason}"
    )
    if mr_response.status_code != 201:
        sys.exit(1)
    content = json.loads(mr_response.content)
    message_string = (
        "Merge Request Created:"
        f"\n\tIID: {content['iid']}, Title: {content['title']}"
        f"\n\tURL: {content['web_url']}"
    )
    if args.webhook_url_file is not None:
        with open(args.webhook_url_file, mode="r") as webhook_file:
            webhook_url = webhook_file.read().strip()
        print("Sending alert to webhook: ...", flush=True)
        webhook_data = json.dumps({"text": message_string})
        webhook_response = requests.post(webhook_url, data=webhook_data)
        if webhook_response.status_code == 200:
            print("Sending alert to webhook: Success!", flush=True)
        else:
            print("Sending alert to webhook: Failed!", flush=True)
    print(message_string, flush=True)


if __name__ == "__main__":
    main()
