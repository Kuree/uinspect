#!/usr/bin/env bash
set -xe
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
ROOT=$(dirname "${DIR}")
PYTHON_VERSION=${PYTHON_VERSION:=cp310-cp310}

docker run -it -d --rm --name manylinux -v ${ROOT}:/uinspect -e PYTHON=/opt/python/${PYTHON_VERSION}/bin/python quay.io/pypa/manylinux2014_x86_64 bash
docker exec manylinux /uinspect/scripts/wheel.sh

docker stop manylinux
