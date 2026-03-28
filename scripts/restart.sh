#!/bin/bash

cd "$(dirname "$0")/.."

echo "Restarting all deployments..."
kubectl rollout restart deployment --all -n streamflow
echo "Done!"

read -p "Press Enter to exit..."