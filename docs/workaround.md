# Workarounds

## Buildbarn Bazel

There is a workaround added for the Buildbarn Bazel build. The issue was that
when running the build with Bazel version 1.1.0, a zip I/O error would appear.

The workaround is in the `docker/bazel/bazel-build-wrapper-crosstools` file.
The line `sed -i 's/\(zip -qd $@\)/chmod +w $@ \&\& \1/' third_party/BUILD`
inserts a `chmod` command which causes the zip I/O error to be avoided.
