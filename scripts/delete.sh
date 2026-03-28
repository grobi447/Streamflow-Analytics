#!/bin/bash

cd "$(dirname "$0")/.."

echo "Deleting all resources..."
kubectl delete namespace streamflow
echo "Done!"

read -p "Press Enter to exit..."