#!/bin/bash

cd "$(dirname "$0")/.."

echo "Stopping all deployments..."
kubectl scale deployment --all --replicas=0 -n streamflow
echo "Done!"

read -p "Press Enter to exit..."