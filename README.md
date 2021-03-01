# YouTube
5 services
Technologies utilisées : API REST: python, FRONT: VueJS, ENCODING: python, ELASTICSEARCH: nodejs, MAILER: nodejs 

# How to use this API
## Docker
Install Docker 
```
run script regen.sh
```
## Usefull commands
```docker ps``` : Show docker process

```docker images``` : Show docker images

```docker exec -it "nom_container" bash``` : Go into the selected container

```docker logs "nom_container"``` : Show container logs

```docker-compose up -d``` : run the docker-compose file

## If you need to install new package, 2 choices :

### Add the new package in file requirements.txt, Delete the docker image and rebuild it by launching the script regen.sh
```docker stop "nom_container"``` : Stop container

```docker rm "nom_container"``` : Remove container

```docker rmi "nom_image"``` : Remove image

### Install the package with pip, then Use pip freeze > requirements.txt
>>>>>>> dockers/develop
