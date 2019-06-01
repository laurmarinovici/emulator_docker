#!/bin/bash

docker run -it --rm -p="127.0.0.1:5000:5000" \
           --mount type=bind,source=/Users/mari009/PNNL_Projects/GitHubRepositories/emulator_docker_fork/julia,destination=/mnt/myapp \
           --mount type=bind,source=/Users/mari009/PNNL_Projects/FY2019/FY19-AdaptiveControl/OptimizationCode/src_new/,destination=/mnt/simulator \
           --network=host --name julia_container julia_image:latest bash