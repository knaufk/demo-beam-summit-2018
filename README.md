# Python Streaming Pipelines with Beam on Flink - Demo 

**This repository contains the demo of my talk at Beam Summit 2018**

## Preparing for the Demo

Follow the steps described in `docker/REAMDME.md` to setup a local containerized environment to run Beam Python Pipelines on Apache Flink.

## Running the Demo

These steps assume you have followed the steps in `docker/README.md` and you have `virtualenvwrapper` (https://virtualenvwrapper.readthedocs.io/en/latest/) installed. 

1. Create a virtualenv containing the required dependencies e.g. by running `mkvirtualenv -r requirements.txt beam`
2. Start the Flink Cluster and Flink Job Server by running `docker-compose up -d` inside the `docker` sub-directory.
3. Run `workon beam && python wordcount.py --sdk_location=container --runner=PortableRunner --experiments=beam_fn_api --job_endpoint=localhost:8099` inside the virtualenv created in the first step.
4. Observe the output by running `docker logs docker_taskmanager_1 -f | grep 'wordcount.process'`.