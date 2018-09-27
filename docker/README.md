## Containerized Portable Flink Runner Environment

Unfortunately, there are a couple of steps involved in the setting this up. 

#### Building Required Beam Images 

First, checkout the `release-2.7.0`-tag of Apache Beam by running
```
git clone git@github.com:apache/beam.git
git checkout origin/release-2.7.0
``` 
Afterwards you need to change line 133 of `FlinkJobServerDriver.java` to `this.artifactServerFactory = artifactServerFactory;` due to a bug in version 2.7.0. Otherwise the Flink Job Server will not be able to start. Then you can build job-server image by running 
```
./gradlew beam-runners-flink_2.11-job-server-container:docker
docker tag <IMAGE ID> flink-job-server:2.7.0-fixed
```
as well as the Python SDK harness container with `./gradlew -p sdks/python/container docker`. 

#### Building the Flink-With-Docker Image

The Flink Taskmanagers need to be able to spawn docker containers, namely the Python SDK harness container. For this we need to build a docker container based on the Flink base image, which has `docker` installed and has a user called `flink`, which is allowed to run containers on the host system.
```
docker build . -t flink-with-docker:1.5.3-scala_2.11 --build-arg DOCKER_GID_HOST=$(grep docker /etc/group | cut -d ':' -f 3)
```