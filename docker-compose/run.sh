\# The contents of this file are covered by APACHE License Version 2.
# See licenses/APACHEV2-LICENSE.txt for more information.

#!/usr/bin/env sh

set -eux

worker="worker-ubuntu16-04"

mkdir -m 0777 "${worker}" "${worker}/build"
mkdir -m 0700 "${worker}/cache"

docker-compose -f docker-compose_buildbarn.yml up -d 
docker-compose -f docker-compose_buildbarn.yml logs --follow &
docker-compose -f docker-compose-bazel.yml up --exit-code-from bazel-client
