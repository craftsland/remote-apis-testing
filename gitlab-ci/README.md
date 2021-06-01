To run our GitLab CI pipelines, we use a custom docker image based on the
`docker:stable` image. To speed up the CI jobs, our custom image has various
dependencies pre-installed.

The docker image is stored in the project's container repository. The name is
"gitlab-ci-image", and the tag is the date when the image was generated.

To update the dependencies and generate a new tag, first update the dockerfile,
then commit the changes and push the changes to GitLab. Next, run a manual
pipeline on the branch containing the updated docker file. When starting the
pipeline, set an environment variable on the pipline with variable name
`MANUAL_TASK` and value `generate-ci-docker-image`.

This will start a pipeline with a job called `generate_ci_docker_image`. This
job will build the new image, and push it to the repository.

To *use* the new docker image, edit the "image" value in .gitlab-ci, for the
test job(s).
