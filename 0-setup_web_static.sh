#!/bin/bash

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null
then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create a fake HTML file for testing
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
nginx_config="location /hbnb_static {\n    alias /data/web_static/current/;\n}"
sudo sed -i "/server_name _;/a $nginx_config" /etc/nginx/sites-available/default

# Restart Nginx and check if it restarts successfully
sudo service nginx restart
if [ $? -ne 0 ]; then
    echo "Nginx restart failed"
    exit 1
fi

# Exit successfully
exit 0
