#/bin/bash
#### -----------------------   PREPARING THE WORKSPACE  -------------------------------
clear
. .env

#### -----------------------   RUNNING THE PROJECT DOCKER  -------------------------------
# get the name of the project docker image 
DOCKER_IMG="${APP_IMG_BUILDER}:${VERSION}"
#### -------   GET VERSION OF THE INSTALLED PYTHON PACKAGES  ---------------------
docker run -it --rm \
	--network host \
	-p "${APP_HOST_PORT}:${APP_SERVER_PORT}" \
	-v "./:/app/build/" \
	-e "PYTHON_VERSION:${PYTHON_VERSION}" \
	--name  "${APP_CNTNR_NAME}-2" \
	"${DOCKER_IMG}" sh -c "cd  /app/build/ && bash dev/pip/run_pip.sh"


