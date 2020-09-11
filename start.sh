#!/usr/bin/env bash

set -a
source /home/ubuntu/repositoryURI
set +a

$(/home/ubuntu/.local/bin/aws ecr get-login --no-include-email --region us-west-2)


export ENVIRONMENT='production'


docker-compose -f /home/ubuntu/production.yml pull django nginx
docker-compose -f /home/ubuntu/production.yml up -d
