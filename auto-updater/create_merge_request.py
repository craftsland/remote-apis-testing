#!/usr/bin/env python3
"""
Pushes the local commits to GitLab as a new branch, then creates a Merge Request to
merge into master.
"""

import datetime
import subprocess

DESCRIBE_TEXT = """
Pushes the local commits to GitLab as a new branch, then creates a Merge Request to
merge into master.
"""


def main():
    """See main module docstring."""
    # Create Branch
    new_branch = f"auto-update/{datetime.date.today()}"
    subprocess.run(["git", "checkout", "-b", new_branch], check=True)
    # Push Branch
    print("Pushing new branch to remote repo.", flush=True)
    subprocess.run(["git", "push", "origin", new_branch], check=True)

    # Create MR
    # (To be implemented)


if __name__ == "__main__":
    main()
