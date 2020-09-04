# Castodia Coding Challenge

This app consists of a Flask server connected to a PostgreSQL DB hosted on an AWS EC2 instance. A web server was hosted on Heroku at https://castodian.herokuapp.com/. 

To test the HTTP requests, see here https://www.postman.com/collections/cb1b6fd854c1fa74c17b for the Postman collection, with default values for ease of use.

Nginx was configured as a reverse proxy for incoming requests, sending them to Gunicorn for handling. I did not use a virtualenv for this project (not the best choice); so I will instead paste my systemd Gunicorn service as well as nginx configuration files below.

Due to time constraints, a number of desirable security and error handling features remain unimplemented. These are documented in the application with comments. 


### gunicorn
```
[Unit]
Description=Instance of Castodia flask 
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/home/tazik/Nextcloud/code/castodia/
Environment="PATH=/usr/bin/"
ExecStart=/usr/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 wsgi:app

[Install]
WantedBy=multi-user.target
```

### nginx

```
server {
    listen 80;
    server_name https://castodian.herokuapp.com/;
location / {
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass http://unix:/home/tazik/Nextcloud/code/castodia/app.sock;
  }
}
```
