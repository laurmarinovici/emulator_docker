#!/bin/bash

DOCKERFILE="Dockerfile.julia"
TESP_REP="laurmarinovici/julia"
TESP_TAG=":latest"
clear
docker build --no-cache --rm\
             --network=host \
             -f ${DOCKERFILE} \
             -t ${TESP_REP}${TESP_TAG} ./
