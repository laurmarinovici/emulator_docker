#!/bin/bash

docker run -it --rm -p="127.0.0.1:5000:5000" \
           --mount type=bind,source=/Users/mari009/PNNL_Projects/GitHubRepositories/emulator_docker/julia,destination=/mnt/myapp \
           --mount type=bind,source=/Users/mari009/PNNL_Projects/GitHubRepositories/emulator_docker_fork/julia/mpc_src,destination=/mnt/mpc \
           --network=host --name julia_container julia_image:latest bash