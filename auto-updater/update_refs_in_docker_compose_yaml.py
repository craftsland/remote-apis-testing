#!/usr/bin/env python3
"""Identifies various references in the docker-compose yaml files, (docker tags,
git commit hashes, etc.) and updates them to the most recent versions. Commits the
updates to each file as a new Git commit."""


import subprocess
from ruamel.yaml import YAML
import get_up_to_date_references

MATRIX_FILE = "../matrix.yml"
COMMIT_AUTHOR = "bot <remote-apis-testing-bot@codethink.co.uk>"


def main():
    """Main function, see module docstring"""
    yaml = YAML(typ="rt")
    with open(MATRIX_FILE, mode="r") as input_stream:
        matrix_yaml = yaml.load(input_stream)
    matrix_projects = matrix_yaml["projects"]

    print("Searching for available updates:", flush=True)
    for project_name, project in matrix_projects.items():
        version_refs_dict = project.get("version_refs", {})
        print("===============================", flush=True)
        print(f"Processing {project_name}", flush=True)
        if version_refs_dict == {}:
            print(
                "!! CANNOT PROCESS !! - Project is not set up for auto-update",
                flush=True,
            )
        else:
            commit_body = update_refs(version_refs_dict)
            if commit_body != "":
                commit_changes(
                    project_name, commit_body, matrix_yaml, MATRIX_FILE, yaml
                )


def update_refs(version_refs_dict):
    """Runs the functions from the function dictionaries, updates the refs if refs need
    updating, and creates a commit message body if anything has been updated."""
    commit_body = ""
    for ref_name, ref_dict in version_refs_dict.items():
        old_ref = ref_dict.get("value", "")
        name_of_update_function = ref_dict.get("update_function", None)
        if name_of_update_function is None:
            print(
                f"- Ignoring {ref_name}, << can't check. Not set up for auto-update.",
                flush=True,
            )
            continue
        update_function = getattr(
            get_up_to_date_references, name_of_update_function, None
        )

        if update_function is None:
            print(
                f"- Ignoring {ref_name}, << the update function"
                f' "{name_of_update_function}" is not recognized.',
                flush=True,
            )
            continue

        print(f"- Checking {ref_name}", flush=True)
        update_args = ref_dict.get("update_args", {})
        new_ref = update_function(**update_args)

        if new_ref != old_ref:
            ref_dict["value"] = new_ref
            ref_dict.move_to_end("value", last=False)
            # ensures value is the first item in a ref_dict

            commit_line_1 = f"Updating {ref_name}"
            commit_line_2 = f"Old ref: {old_ref}\tNew ref: {new_ref}"
            print(f"  {commit_line_1}\t{commit_line_2}", flush=True)
            commit_body += f"\n{commit_line_1}\n{commit_line_2}"

    return commit_body


def commit_changes(project_name, commit_body, matrix_yaml, matrix_file, yaml):
    """Writes the updates to the matrix file, and
    creates a new commit to record the updated refs."""
    with open(MATRIX_FILE, mode="w") as output_stream:
        yaml.dump(matrix_yaml, output_stream)
    commit_subject = f"auto-update refs: {project_name}\n"
    commit_message = commit_subject + commit_body
    subprocess.call(["git", "add", matrix_file])
    subprocess.call(
        ["git", "commit", f"--author={COMMIT_AUTHOR}", "-m", commit_message]
    )


if __name__ == "__main__":
    main()
