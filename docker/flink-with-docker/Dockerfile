FROM flink:1.8.0-scala_2.11

ARG DOCKER_GID_HOST

RUN groupadd -for -g $DOCKER_GID_HOST docker

RUN apt-get update; \
  apt-get -y install apt-transport-https ca-certificates curl gnupg software-properties-common; \
  curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -; \
  apt-key fingerprint 0EBFCD88; \
  add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/debian \
       $(lsb_release -cs) \
       stable" ;\
  apt-get update; \
  apt-get -y install docker-ce

RUN usermod -aG docker flink
