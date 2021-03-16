#!/usr/bin/env bash

HELP_TEXT='This script will run pydantic-wip examples in a docker container. See README.md for
more information on running examples.

Use: ./run-example.sh -e \$EXAMPLE_NAME [OPTIONS]

Required:
  --example / -e : The subdirectory under "examples" that you want to run.

Options:
  --build / -b : Re-build the image before running.
  --mount / -m : Live-mount the example code onto the container, so that you can see
                 results as you fiddle with things.
  --help / -h  :  Display this mesage and exit.'

BUILD=
LIVE_MOUNT=

while (( $# ))
do
  case $1 in
    --build|-b)
      BUILD=1
      ;;
    --example|-e)
      shift
      EXAMPLE=$1
      ;;
    --mount|-m)
      shift
      LIVE_MOUNT=1
      ;;
    --help|-h)
      echo "${HELP_TEXT}"
      exit 1
  esac
  shift
done

test -n "${BUILD}" && docker build .
test -n "${LIVE_MOUNT}" && \
  export LIVE_MOUNT="--volume $(pwd)/examples:/pydantic-examples/examples"

if [[ -z "${EXAMPLE}" ]]
then
  echo "No example provided. Please provide an example directory name."
  exit 1
fi

EXAMPLE_PATH=$(pwd)/examples/${EXAMPLE}

source $EXAMPLE_PATH/.example.sh

set -ex
docker run $DOCKER_RUN_ARGS -it pydantic-examples $DOCKER_RUN_COMMAND