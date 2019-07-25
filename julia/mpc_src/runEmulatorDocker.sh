#!/bin/bash

docker run -it --rm -p="127.0.0.1:5000:5000" \
           --mount type=bind,source=/Users/mari009/PNNL_Projects/GitHubRepositories/emulator_docker_fork/emulatorExamples/,destination=/mnt/examples \
           --name=jmodelica_docker laurmarinovici/building_control_emulator:latest bash

# --network=host 