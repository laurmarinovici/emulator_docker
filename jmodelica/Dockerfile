FROM michaelwetter/ubuntu-1604_jmodelica_trunk

ENV ROOT_DIR /usr/local
ENV JMODELICA_HOME $ROOT_DIR/JModelica
ENV IPOPT_HOME $ROOT_DIR/Ipopt-3.12.4
ENV SUNDIALS_HOME $JMODELICA_HOME/ThirdParty/Sundials
ENV SEPARATE_PROCESS_JVM /usr/lib/jvm/java-8-openjdk-amd64/
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV PYTHONPATH $PYTHONPATH:$JMODELICA_HOME/Python:$JMODELICA_HOME/Python/pymodelica
ENV USER_NAME=developer

USER root

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/archives/* && \
    echo "===== PYTHON VERSION =====" && \
    python --version && \
    echo "===== PIP VERSION =====" && \
    pip --version && \
    echo "===== install FLASK-RESTFUL =====" && \
    pip install --user flask-restful && \
    echo "===== current PYTHON modules =====" && \
    pip list --format=columns && \
    echo "root:jmodelica" | chpasswd

USER ${USER_NAME}
WORKDIR $HOME