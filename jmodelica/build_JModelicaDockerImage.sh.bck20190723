#!/bin/bash

DOCKERFILE="Dockerfile"
ARG_NAME="testcase"
ARG_VALUE="testcase3"
REPO="boptest_${ARG_VALUE}"
TAG=":latest"

clear
docker build --no-cache --rm \
             --network=host \
             --build-arg ${ARG_NAME}=${ARG_VALUE} \
             -f ${DOCKERFILE} \
             -t ${REPO}${TAG} ./