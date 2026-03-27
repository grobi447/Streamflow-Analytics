#!/bin/bash

echo "Stopping StreamFlow Analytics..."
kubectl delete namespace streamflow
echo "Done!"

read -p "Press Enter to exit..."