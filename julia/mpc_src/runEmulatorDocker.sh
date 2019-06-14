#!/bin/bash

docker run -it --rm -p="127.0.0.1:5000:5000" \
           --mount type=bind,source=/Users/mari009/PNNL_Projects/GitHubRepositories/emulator_docker/jmodelica/,destination=/mnt/master \
           --mount type=bind,source=/Users/mari009/PNNL_Projects/GitHubRepositories/emulator_docker_fork/jmodelica/,destination=/mnt/fork \
           --network=host --name=jmodelica boptest_testcase3 bash