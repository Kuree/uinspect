#!/usr/bin/env bash
set -xe
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
ROOT=$(dirname "${DIR}")

cd ${ROOT}
${PYTHON} setup.py bdist_wheel
