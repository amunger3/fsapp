#!/bin/bash

# Load Python virtual environment
source ./env/bin/activate
echo "env :: $(which python)"

# Set config environment vars
export FLASK_APP=dashapp
export FLASK_ENV=development
echo "vars :: ${FLASK_APP} | ${FLASK_ENV}"