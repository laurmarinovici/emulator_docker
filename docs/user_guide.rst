Emulator platform
*****************
The building emulator is given as a Functional Mock-up Unit (FMU) and simulated using `JModelica`_. JModelica, as the tool to simulate and analyze the building emulator behavior, has been packaged on a Ubuntu 16.04.5 LTS machine in a Docker container. Hence, in order to download, access and run the JModelica-specialized container, Docker needs to be installed on the host machine.

.. _JModelica: https://jmodelica.org

Docker Container
================
For Windows 10 and Mac OS, there are specific versions of `Docker desktop`_, that is `Docker desktop for Windows`_, and `Docker desktop for Mac`_. On Ubuntu (Linux), installing Docker is less straight forward, and the procedure coudl follow the details below.

.. _`Docker desktop`: https://www.docker.com/products/docker-desktop
.. _`Docker desktop for Windows`: https://hub.docker.com/editions/community/docker-ce-desktop-windows
.. _`Docker desktop for Mac`: https://hub.docker.com/editions/community/docker-ce-desktop-mac


File `Script to install Docker CE on Ubuntu`_, which presents what the docker installation site shows at `Docker installation`_, can be used as helper to download and install Docker CE on Ubuntu.

.. _Script to install Docker CE on Ubuntu: https://github.com/GRIDAPPSD/gridappsd-docker/blob/master/docker_install_ubuntu.sh
.. _Docker installation: https://docs.docker.com/install/linux/docker-ce/ubuntu/

.. code::

  #!/bin/bash

  # Environment variables you need to set so you don't have to edit the script below.
  DOCKER_CHANNEL=stable
  DOCKER_COMPOSE_VERSION=1.18.0

  # Update the apt package index.
  sudo apt-get update

  # Install packages to allow apt to use a repository over HTTPS.
  sudo apt-get install -y \
      apt-transport-https \
      ca-certificates \
      curl \
      software-properties-common \
      vim

  # Add Docker's official GPG key.
  curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | sudo apt-key add -

  # Verify the fingerprint.
  sudo apt-key fingerprint 0EBFCD88

  # Pick the release channel.
  sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
    $(lsb_release -cs) \
    ${DOCKER_CHANNEL}"

  # Update the apt package index.
  sudo apt-get update

  # Install the latest version of Docker CE.
  sudo apt-get install -y docker-ce

  # Allow your user to access the Docker CLI without needing root.
  sudo /usr/sbin/usermod -aG docker $USER

  # Install Docker Compose.
  curl -L https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-`uname -s`-`uname -m` -o /tmp/docker-compose
  sudo mv /tmp/docker-compose /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  sudo chown root:root /usr/local/bin/docker-compose

The script also installs Docker Composer, used to define and run a multi-container Docker application. See `Compose overview`_.

.. _Compose overview: https://docs.docker.com/compose/overview/

**Warning.** To be able to run the Docker CLI without needing root, you need a reboot.

Getting the JModelica emulator docker image
-------------------------------------------

**Note.** The following procedures are related to Mac OS and Ubuntu.

Once Docker desktop is installed on the host computer, to get access to the JModelica container, one could follow the steps below. Details on the Docker commands can be found on the `Docker documentation`_ page.

.. _Docker documentation: https://docs.docker.com

1. Open a terminal window.

2. At the terminal prompt type

.. code::

  docker pull <..... I NEED A DOCKER HUB LINK ......>

The docker image will be downloaded on the host computer.

3. To inspect the Docker images downloaded type

.. code::

  docker images

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

  **Code documentation -** *testcase.py*

  .. automodule:: testcase

  - *Acquire the list of inputs the emulator accepts as control signals*

    The emulator inputs are pairs of 2 values for each control signal:

    - *<name>_activate* - that can take 0 or 1 values indicating that particular input is going to be used for control with the given value rather than the default value

    - *<name>_u* - that represents the actual input value that the control designer calculates

  .. autoclass:: testcase.TestCase
    :members: get_inputs

  - *Acquire the list of measurements exposed by the emulator*

  .. autoclass:: testcase.TestCase
    :members: get_measurements

  - *Advance the emulator simulation one step further after providing a set of control inputs to it with*

  .. autoclass:: testcase.TestCase
    :members: advance

  - *Obtain the name of the emulator*

  .. autoclass:: testcase.TestCase
    :members: get_name

  - *Obtain the simlation time step in seconds*

  .. autoclass:: testcase.TestCase
    :members: get_step

  - *Set the simulation time step in seconds*

  .. autoclass:: testcase.TestCase
    :members: set_step

  - *Obtain full trajectories of measurements and control inputs*

  .. autoclass:: testcase.TestCase
    :members: get_results

  - *Obtain key performance indicator (kpi)*

  .. autoclass:: testcase.TestCase
    :members: get_kpis

- instantiate the emulator and define the REST API to interact with it through different requests

  **Code documentation -** *restapi.py*

  .. automodule:: restapi

  .. autoclass:: restapi.Advance
    :members:

  .. autoclass:: restapi.Inputs
    :members:
  
  .. autoclass:: restapi.Measurements
    :members:
  
  .. autoclass:: restapi.Results
    :members:
  
  .. autoclass:: restapi.KPI
    :members:
  
  .. autoclass:: restapi.Name
    :members:

Running emulator simulation - Example
=====================================

1. Open the Ubuntu terminal on a distribution that includes Docker.

2. Download the JModelica Docker

.. code::

  docker pull <..................>

3. Running

.. code::

  docker images

should return something similar to

+-------------------+----------+------------------+----------------+--------------+
| REPOSITORY        | TAG      | IMAGE ID         | CREATED        | SIZE         |
+===================+==========+==================+================+==============+
| boptest_testcase3 | latest   | 52bae37ee322     | 3 weeks ago    | 1.27GB       |
+-------------------+----------+------------------+----------------+--------------+

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

  python restapi.py

which will now wait for requests to access the emulator.


