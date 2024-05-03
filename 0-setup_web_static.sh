#!/usr/bin/env bash

# This script sets up web servers for web_static deployment

# Variables
NGINX_CONFIG_FILE="/etc/nginx/sites-available/default"
WEB_STATIC_PATH="/data/web_static"
WEB_STATIC_CURRENT="${WEB_STATIC_PATH}/current"
WEB_STATIC_RELEASES="${WEB_STATIC_PATH}/releases"
WEB_STATIC_SHARED="${WEB_STATIC_PATH}/shared"
TEST_RELEASE="${WEB_STATIC_RELEASES}/test"
USER="your_existing_user"  # Replace with an existing user on your system

# Update package lists
sudo apt-get update

# Install Nginx if not already installed
if ! dpkg -s nginx >/dev/null 2>&1; then
    sudo apt-get -y install nginx
fi

# Install UFW if not already installed
if ! dpkg -s ufw >/dev/null 2>&1; then
    sudo apt-get -y install ufw
    sudo ufw allow 'Nginx HTTP'
fi

# Create necessary directories
sudo mkdir -p "${TEST_RELEASE}" "${WEB_STATIC_SHARED}"

# Create a basic HTML file
sudo bash -c 'printf "<html>\n<head>\n</head>\n<body>\nHolberton School\n</body>\n</html>" > '"${TEST_RELEASE}"'/index.html'

# Create a symbolic link to the test release
sudo ln -sf "${TEST_RELEASE}" "${WEB_STATIC_CURRENT}"

# Change ownership of the web_static directory
sudo chown -R "${USER}:${USER}" "${WEB_STATIC_PATH}"

# Configure Nginx to serve static files
sudo sed -i "/listen 80 default_server/a location /hbnb_static/ { alias ${WEB_STATIC_CURRENT}/; }" "${NGINX_CONFIG_FILE}"

# Restart Nginx service
sudo service nginx restart
