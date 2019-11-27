#!/bin/bash
if [ $# -lt 1 ]
then
  echo "Expected BADGE_URL"
  echo "Usage: badge_script.sh BADGE_URL"
  exit 1
fi

get_badge() {
  if [ ! -f "badges/${SERVER}-${CLIENT}-deployed.svg" ]; then
    curl -o badges/${SERVER}-${CLIENT}-deployed.svg $BADGE_URL/${SERVER}-failed-red.svg
  fi
}

BADGE_URL=$1

# Bazel
CLIENT=bazel
for SERVER in buildbarn buildfarm buildgrid
do
  get_badge
done

# Buildstream
CLIENT=buildstream
for SERVER in buildgrid
do
  get_badge
done

# recc
CLIENT=recc
for SERVER in buildgrid
do
  get_badge
done

# Times
for SERVER in buildbarn buildfarm buildgrid
do
  if [ ! -f "badges/${SERVER}-time.svg" ]; then
    curl -o badges/${SERVER}-time.svg $BADGE_URL/${SERVER}_bazel-failed-red.svg
  fi
done

# Incremental times
for SERVER in
do
  if [ ! -f "badges/${SERVER}-incremental-time.svg" ]; then
    curl -o badges/${SERVER}-incremental-time.svg $BADGE_URL/${SERVER}_bazel-failed-red.svg
  fi
done

# Concurrency-1 times
for SERVER in buildbarn buildfarm
do
  if [ ! -f "badges/${SERVER}-concurrency-1-time.svg" ]; then
    curl -o badges/${SERVER}-concurrency-1-time.svg $BADGE_URL/${SERVER}_bazel-failed-red.svg
  fi
done

# Incremental concurrency-1 times
for SERVER in
do
  if [ ! -f "badges/${SERVER}-concurrency-1-incremental-time.svg" ]; then
    curl -o badges/${SERVER}-concurrency-1-incremental-time.svg $BADGE_URL/${SERVER}_bazel-failed-red.svg
  fi
done
