#!/bin/bash

docker run -it --rm -p="127.0.0.1:5000:5000" \
           --mount type=bind,source=/home/tesp/repositories/emulator_docker/jmodelica/,destination=$HOME/master \
           --mount type=bind,source=/home/tesp/repositories/emulator_docker_fork/jmodelica/,destination=$HOME/fork \
           --network=host --name=jmodelica_docker laurmarinovici/building_control_emulator:latest bash
