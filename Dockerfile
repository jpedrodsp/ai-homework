FROM ubuntu:22.04 AS baseimage

# Copy the current directory contents into the container at /app
WORKDIR /app
COPY . /app

# Install Python 3 with pip and venv
RUN apt update -y && \
apt install -y python3 python3-pip python3-venv

# Create python virtual environment with venv
RUN python3 -m venv .venv
RUN source .venv/bin/activate

# Install needed packages in requirement.txt
RUN python install -r requirements.txt

# Specify shell and command to run
SHELL ["/bin/bash", "-c"]
CMD ["echo", "Hello World"]