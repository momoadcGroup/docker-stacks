name: Build and push pyspark jupyter notebook image


on:
  workflow_dispatch:
    inputs:
      spark_version:
        description: 'The spark version to download and build (e.g. 3.2.0)'
        required: true
        type: string

      hadoop_version:
        description: 'The hadoop version spark was compiled with (e.g. 3.2)'
        required: true
        type: string

      python_version:
        description: 'The python version to build (e.g. py39)'
        required: true
        type: string

      push_container_flag:
        description: 'Whatever to push the image'
        required: true
        type: boolean

      ref:
        description: 'Git ref to a branch/tag/hash'
        required: true
        type: string

      pyspark_notebook_tag:
        description: 'The tag to give to the pyspark notebook image'
        required: true
        type: string

env:
  REGISTRY: ghcr.io

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
        with:
          ref: "${{ github.event.inputs.ref }}"

      - name: Set env variables
        run: |
             export spark_download_url="https://archive.apache.org/dist/spark/spark-${{ github.event.inputs.spark_version }}/spark-${{ github.event.inputs.spark_version }}-bin-hadoop${{ github.event.inputs.hadoop_version }}.tgz"
             echo "SPARK_CHECKSUM=`curl ${{ env.spark_download_url }}.sha512 | sed 's/.*://' | tr -d ' \n' | rev | cut -c 1- | rev`" >> $GITHUB_ENV
             echo "BASE_IMAGE_NAME=${{ env.REGISTRY }}/${{ github.repository }}/jupyter-notebook:BUILD_TAG" >> $GITHUB_ENV

      - name: Log into registry
        if: github.event.inputs.push_container_flag == 'true'
        uses: docker/login-action@v1
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}


      - name: Build jupyter notebook
        uses: docker/build-push-action@v2
        with:
          context: ./base-notebook
          push: false
          tags: "${{ github.repository }}/jupyter-notebook:BUILD_TAG"
          build-args:
            # Fix OpenShift permissions
            - NB_GID=0
            - PYTHON_VERSION="${{ github.event.inputs.python_version }}"

      # github.repository as <account>/<repo>
      - name: Build and push pyspark notebook
        uses: docker/build-push-action@v2
        with:
          context: ./pyspark-notebook
          push: github.event.inputs.push_container_flag == 'true'
          tags: "${{ github.repository }}/pyspark-notebook:${{ github.event.inputs.pyspark_notebook_tag }}"
          build-args:
            - BASE_CONTAINER="${{ env.BASE_IMAGE_NAME }}"
            - spark_version="${{ github.event.inputs.spark_version }}"
            - hadoop_version="${{ github.event.inputs.hadoop_version }}"
            - spark_checksum="${{ env.SPARK_CHECKSUM }}"
