## Containerized Portable Flink Runner Environment

You need to build a couple of images for this dockerized Beam on Flink setup.

#### Building Required Beam Images 

First, checkout `release-2.13.0` of Apache Beam by running
```
git clone git@github.com:apache/beam.git
git checkout origin/release-2.13.0
``` 
Afterwards you can build the job server image by running
```
./gradlew -p runners/flink/1.8/job-server-container docker -Pdocker-repository-root=beam -Pdocker-tag=2.13.0
```
as well as the Python SDK harness container: 

```
./gradlew -p sdks/python/container docker
```

#### Building the Flink-With-Docker Image

The Flink TaskManagers need to be able to spawn docker containers, namely the Python SDK harness container. For this we need to build a docker image based on the Flink image, which has `docker` installed and a user called `flink`, which is allowed to run containers on the host system.
```
docker build . -t flink-with-docker:1.8.0-scala_2.11 --build-arg DOCKER_GID_HOST=$(grep docker /etc/group | cut -d ':' -f 3)
```