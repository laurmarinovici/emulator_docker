JModelica Docker
================

Getting the JModelica emulator docker image
-------------------------------------------

**Note.** The following procedures are related to Mac OS and Ubuntu.

Once Docker desktop is installed on the host computer, to get access to the JModelica container, one could follow the steps below. Details on the Docker commands can be found on the `Docker documentation`_ page.

.. _Docker documentation: https://docs.docker.com

1. Open a terminal window.

2. At the terminal prompt type

.. code::

  docker pull laurmarinovici/building_control_emulator:latest

The docker image will be downloaded on the host computer.

3. To inspect the Docker images downloaded type

.. code::

  docker images

should return a list of Docker images, which should include something similar to

+-------------------------------------------+----------+------------------+----------------+--------------+
| REPOSITORY                                | TAG      | IMAGE ID         | CREATED        | SIZE         |
+===========================================+==========+==================+================+==============+
| blaurmarinovici/building_control_emulator | latest   | 04f1b11d5bd6     | 31 hours ago   | 1.69GB       |
+-------------------------------------------+----------+------------------+----------------+--------------+

4. To instantiate the Docker container, run

.. code::

  docker run -it --rm -p="127.0.0.1:5000:5000" \
           --mount type=bind,source=<path to host computer folder to bind with container folder>,destination=<path to folder in the container binded to host folder> \
           --network=host --name=<container name> <image name> bash

5. Once the container has been created, it should show up listed when running

.. code::

  docker ps -a

Inside the JModelica Docker container
-------------------------------------

.. _JModelica Docker container:

  .. figure:: images/emulatorDockerDiagram.png
    :scale: 50 %

    Figure 1. Emulator Docker diagram

Inside the `JModelica Docker container`_, the emulator is simulated using a `REST`_ (REpresentational State Transfer) API to

.. _REST: https://restfulapi.net

- configure the test case, that is specify the emulator to be simulated and set the simulation time step in seconds (config.py)

- implement a test case Python class that defines the API used by the REST requests to perform functions such as advancing the simulation, retrieving test case information, and calculating and reporting results

  **Code documentation -** *emulatorSetup.py*

  .. automodule:: emulatorSetup

  - *Acquire the list of inputs the emulator accepts as control signals*

    The emulator inputs are pairs of 2 values for each control signal:

    - *<name>_activate* - that can take 0 or 1 values indicating that particular input is going to be used for control with the given value rather than the default value

    - *<name>_u* - that represents the actual input value that the control designer calculates

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: get_inputs

  - *Acquire the list of measurements exposed by the emulator*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: get_measurements

  - *Advance the emulator simulation one step further after providing a set of control inputs to it with*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: advance

  - *Obtain the name of the emulator*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: get_name

  - *Obtain the simlation time step in seconds*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: get_step

  - *Set the simulation time step in seconds*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: set_step

  - *Obtain full trajectories of measurements and control inputs*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: get_results

  - *Obtain key performance indicator (kpi)*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: get_kpis

- instantiate the emulator and define the REST API to interact with it through different requests

  **Code documentation -** *startREST.py*

  .. automodule:: startREST

  .. autoclass:: startREST.Advance
    :members:

  .. autoclass:: startREST.Inputs
    :members:
  
  .. autoclass:: startREST.Measurements
    :members:
  
  .. autoclass:: startREST.Results
    :members:
  
  .. autoclass:: startREST.KPI
    :members:
  
  .. autoclass:: startREST.Name
    :members:

Running emulator simulation - Example
=====================================

.. _Simulation setup:

  .. figure:: images/simulationDockerDiagram.png
    :scale: 30 %

    Figure 2. Simulation setup diagram

1. Open the Ubuntu terminal on a distribution that has Docker installed.

2. Download the JModelica Docker

.. code::

  docker pull laurmarinovici/building_control_emulator:latest

3. Running

.. code::

  docker images



4. Create the JModelica Docker container by running

.. code::

  docker run -it --rm -p="127.0.0.1:5000:5000" \
           --mount type=bind,source=/Users/mari009/PNNL_Projects/GitHubRepositories/emulator_docker/jmodelica/,destination=/mnt/master \
           --mount type=bind,source=/Users/mari009/PNNL_Projects/GitHubRepositories/emulator_docker_fork/jmodelica/,destination=/mnt/fork \
           --network=host --name=jmodelica boptest_testcase3 bash

which will create a Docker container named *jmodelica* from *boptest_testcase3* image, and bind 2 host computer folders to 2 container folders, specifically, the master branch of the emulator GitHub repository to */mnt/master*  and a forked version to */mnt/fork/*. This way we have access to any file in the local host folders, including the emulator FMU, and any development done on any file of the binded local folders would automatically be available in the container.

5. After running the docker command from point 4, we get acces to the bash command inside the container. Navigate to one of the binded folders to access the configuration and the REST API files. In *config.py*, make sure line

.. code::

  'fmupath'  : './testcase3/models/wrapped.fmu', 

points to the correct location and name of the emulator FMU.

6. Back at the terminal prompt, launch the application by starting the REST API

.. code::

  python startREST.py

which will now wait for requests to access the emulator to update control actions or request measurements.


