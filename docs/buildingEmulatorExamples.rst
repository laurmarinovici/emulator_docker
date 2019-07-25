Building emulator examples
==========================

On `Building Control Emulator`_ Github repository at *https://github.com/SenHuang19/BuildingControlEmulator*:

.. _Building Control Emulator: https://github.com/SenHuang19/BuildingControlEmulator

- folder *emulatorExamples* contains:

  - *emulatorSetup.py* - to implement the emulatorSetup class

  - *startREST.py* - to load the building emulator/FMU and start the REST server

  - folder *models* that includes the building emulators given as FMU files

  This folder needs to be bound to a folder inside the container to have access to the FMU to simulate.

- folder *simulationExamples* contains:

  - *runSimulation.py* - script to be run from the host computer to simulate the emulator inside the docker, control it if need be, get results, or hatever else the developer wants to add. This script is to be called using

  .. code:

    python runSimulation.py -u "http://0.0.0.0:5000" -d 200 -o 0 -l 1200 -s 300

  or

  .. code:

    python runSimulation.py --url="http://0.0.0.0:5000" --dayOfYear=200 --dayOffset=0 --simDuration=1200 --fmuStep=300

  where

  - *-u*, *--url* represents the 