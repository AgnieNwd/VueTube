#!/bin/bash

docker stop t_python t_encoder t_node t_mailer t_rabbit #t_db
docker rm t_python t_encoder t_node t_mailer t_rabbit #t_db

#node esdocker/index.js

docker-compose up -d #--build --force-recreate
