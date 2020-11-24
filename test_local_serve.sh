#!/bin/bahs
container_id=$(docker ps | grep iris-model | cut -f 1 -d ' ')
docker cp output/* $container_id:/opt/ml/model
curl -X POST -H 'Content-Type: text/csv' -d @data/smoketest/iris.csv http://localhost:8080/invocations