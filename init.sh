#!/bin/bash

source ./env/bin/activate
echo "env :: $(which python)"

export FLASK_APP=dashapp
export FLASK_ENV=development
echo "vars :: ${FLASK_APP} | ${FLASK_ENV}"