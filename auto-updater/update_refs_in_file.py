"""Decorator function for updating refs in a file.
   Takes a function for finding the most recent version of one reference.
   Returns a function that will iterate through a dictionary of update-instructions.
   See function docstring for details."""

import re
import subprocess
import os.path

COMMIT_AUTHOR = "bot <remote-apis-testing-bot@codethink.co.uk>"


def update_refs_in_file_and_commit_changes(file_data):
    """Takes a dictionary with information about the file that need to be updated, and
    the references (tags, hashes, versions, etc) that need to be kept up to date.

    - reads the relevant file,
    - finds the current versions of each ref (as listed in the file),
    - uses some other function to find the most up-to-date version of that ref,
    - edits the file if anything needs updating,
    - commits the changes to the git repository, with a suitable commit message."""

    file_basename = os.path.basename(file_data.filename)
    print("===============================", flush=True)
    print(f"Processing {file_data.name}", flush=True)
    print(f"Reading file {file_basename}", flush=True)
    with open(file_data.filename, mode="r") as openfile:
        filetext = openfile.read()
    commit_body = ""
    for ref in file_data.refs:
        display_name = ref.get("display_name", ref["match_prefix"])
        print(f"- Checking {display_name}", flush=True)
        # match regular expression means:
        #    The match prefix, followed by optional spaces
        #    Followed by a sequence of non-space characters (the actual result)
        #    We extract the actual result with .group(1)
        match_expr = f"{ref['match_prefix']}" + r"[\s]*([^\s]+)"
        existing_ref = re.search(match_expr, filetext)
        if existing_ref:
            function = ref.pop("function")
            latest_ref = function(**ref)
            if latest_ref != existing_ref.group(1):
                commit_line_1 = f"Updating {display_name}"
                commit_line_2 = (
                    f"Old ref: {existing_ref.group(1)}\tNew ref: {latest_ref}"
                )
                print(f"  {commit_line_1}\t{commit_line_2}", flush=True)
                replace_text = existing_ref.group().replace(
                    existing_ref.group(1), latest_ref
                )
                filetext = filetext.replace(existing_ref.group(), replace_text)
                commit_body += f"\n{commit_line_1}\n{commit_line_2}"
    if commit_body:
        with open(file_data.filename, mode="w") as openfile:
            openfile.write(filetext)
        commit_subject = f"auto-update refs: {file_data.name}\n"
        commit_message = commit_subject + commit_body
        subprocess.call(["git", "add", file_data.filename])
        subprocess.call(
            ["git", "commit", f"--author={COMMIT_AUTHOR}", "-m", commit_message]
        )
    else:
        print("  No changes made", flush=True)
