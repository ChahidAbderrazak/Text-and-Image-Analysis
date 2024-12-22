#!/bin/bash

# Uncomment the desired command
command="python src/web_chat.py " # chatbot
command="jupyter lab --allow-root --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token='' --NotebookApp.password='' "

# load the environemnt variables
. .env
. .env_CHATBOT

# get the name of the project docker image 
DOCKER_IMG="${APP_IMG_BUILDER}:${VERSION}"
docker system prune -f

#### ----------------   SHOW/UPDATE THE URLs/IP-ADRESSES -------------------------
# docker system prune -f
bash bash/4-open-app-servers-in-browser.sh

#### -----------------------   RUNNING THE PROJECT DOCKER  -------------------------------
# run the the project container(s)
echo && echo "[${PROJECT_NAME}][Docker][dev] running the development container(s)..."
docker run -it --rm \
           --network host \
           -p "${APP_HOST_PORT}:${APP_SERVER_PORT}" \
           -p "8888:8888" \
           -v "./:/app/" \
           "${DOCKER_IMG}" sh -c \
           "${command}"
        #    --name  "${APP_CNTNR_NAME}_dev" \

# show all running dockers 
docker ps
