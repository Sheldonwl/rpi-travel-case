#!/bin/sh

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "You need to supply a version tag"
    echo "For example: ./build.sh 0.0.1"
else
docker build . -t clear-pixels
docker tag clear-pixels sheldonwl/blinkt-clear-pixels:$1
docker push sheldonwl/blinkt-clear-pixels:$1
fi
