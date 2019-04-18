#!/bin/bash

DOCKERFILE="Dockerfile"
REPO="julia_image"
TAG=":latest"
clear
docker build --no-cache --rm\
             --network=host \
             -f ${DOCKERFILE} \
             -t ${REPO}${TAG} ./