#!/bin/bash

docker run -it --rm -p="127.0.0.1:5000:5000" \
           --mount type=bind,source=/home/tesp/repositories/emulator_docker_fork/julia/,destination=/mnt/myapp \
           --mount type=bind,source=/home/tesp/repositories/emulator_docker_fork/julia/mpc_src/,destination=/mnt/mpc \
           --network=host --name julia_docker laurmarinovici/julia_1.1.1:latest bash
