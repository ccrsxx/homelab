#!/usr/bin/env bash

. `dirname $0`/normalize_path.sh

source venv/bin/activate

python script/docker.py

deactivate

