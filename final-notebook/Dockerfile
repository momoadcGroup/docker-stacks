FROM ghcr.io/momoadcgroup/docker-stacks/pyspark-notebook:spark-3.2.1-hadoop-3.2-py36

COPY requirements.txt /tmp
USER root

RUN apt-get update && \
    apt-get install -y git graphviz && \
    mamba uninstall jupyterlab && \
    pip install -r /tmp/requirements.txt --no-cache-dir && \
    jupyter lab build
    