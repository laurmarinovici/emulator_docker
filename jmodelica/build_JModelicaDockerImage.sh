#!/bin/bash

DOCKERFILE="Dockerfile"
REPO="laurmarinovici/building_control_emulator"
TAG=":latest"

clear
docker build --no-cache --rm \
             --network=host \
             -f ${DOCKERFILE} \
             -t ${REPO}${TAG} ./