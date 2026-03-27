#!/bin/bash

cd "$(dirname "$0")/.."

echo "Starting port forwarding..."
echo "Press Ctrl+C to stop"
echo ""

kubectl port-forward svc/vertica 5433:5433 -n streamflow &
kubectl port-forward svc/kafka 9092:9092 -n streamflow &
kubectl port-forward svc/kafka-ui 8080:8080 -n streamflow &

wait