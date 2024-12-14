
ARG OPENJDK_VERSION=openjdk:8-slim-buster
ARG PYTHON_VERSION=python:3.11
# python
FROM $PYTHON_VERSION AS py3
ENV PYTHONUNBUFFERED 1

# java
FROM $OPENJDK_VERSION
COPY --from=py3 / /

ARG APP_SERVER_PORT=8383

# FROM ubuntu:20.04
# ENV DEBIAN_FRONTEND=noninteractive

# Add user
RUN adduser --quiet --disabled-password appuser && usermod -a -G audio appuser

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# This fix: qt.qpa.plugin: Could not load the Qt platform plugin "xcb"
ENV QT_DEBUG_PLUGINS=1

# update the packages
RUN apt-get update -y

# copy the code files
WORKDIR /app
COPY src /app/src
COPY config /app/config
COPY requirements.txt .
COPY setup.py .
COPY README.md .

# #!recheck: Install Python 3, PyQt5
# RUN apt-get install -y python3-pip python3-pyqt5 

# Install pip requirements
COPY requirements.txt .
COPY setup.py .
# RUN pip3 install -r requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# # #!recheck:2 avoid PyQT issue :  no Qt platform plugin could be initialized
# RUN pip3 uninstall -y opencv-python

EXPOSE $APP_SERVER_PORT
CMD ["python3", "main.py", "--cfg", "config.yml"]