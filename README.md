# facil-wg

`facil-wg` is a project designed to help you manage a Wireguard VPN with ease. It provides a simple web interface built with a Flask Python application, allowing you to manage connected users effortlessly. The project is set up to be installed in a Docker container for easy deployment.

## Features

- **Simple Web Interface:** Manage your Wireguard VPN users through an intuitive web interface.
- **Dockerized:** Easily deploy the application in a Docker container.
- **User Management:** Add, remove, and monitor users connected to your VPN.

## Installation

Follow these steps to install and run `facil-wg` on your server or device.

### 1. Run the Docker Container
Once the image is built, you can run the container with the following command:

```bash
docker run -d \
    -p 51820:51820/udp \
    -p 80:8080 \
    --cap-add=NET_ADMIN \
    --cap-add=SYS_MODULE \
    --name wg \
    -e PASSWORD="Your password utf-8" \
    -e HOST="Your public ip or your host domain name (DDNS)" \
    ghcr.io/ricardo-ha/facil-wg  

```
### 2. Access the Web Interface
After the container is running, you can access the web interface through your browser by navigating to http://<Your_Host_or_IP>.

# Based On
This project is based on [wg-easy](https://github.com/wg-easy/wg-easy).

The web interface was developed with help from [screenshot-to-code](https://github.com/abi/screenshot-to-code).