#!/bin/bash

set +v

mkdir solrdata;

sudo chown 8983:8983 solrdata;

sudo docker-compose up -d;

echo "Waiting for docker init..."
sleep 10

sudo ./create_core.sh