#!/usr/bin/env bash

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary folders
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_content="server {
    listen 80;
    server_name localhost;

    location /hbnb_static {
        alias /data/web_static/current/;
    }

    location / {
        try_files \$uri \$uri/ /index.html;
    }
}"

echo "$config_content" | sudo tee /etc/nginx/sites-available/default > /dev/null

# Restart Nginx
sudo service nginx restart

exit 0
