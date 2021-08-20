# **RinZ Music API**

## Environment
- docker
- docker-compose

### Notes
- Changes in docker-compose.yml: exposed port, image name, container name
- Changes in supervisord.conf: log files' location

### Use with docker, docker-compose
JUST RUN: `> docker-compose up -d --build`

## Health check
```curl -i http://localhost:5000/healthcheck```

## Container env config:
```/webapps/.env```