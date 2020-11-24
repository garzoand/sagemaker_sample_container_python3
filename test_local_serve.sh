#!/bin/bash
curl -X POST -H 'Content-Type: text/csv' -d @data/smoketest/iris.csv http://localhost:8080/invocations
