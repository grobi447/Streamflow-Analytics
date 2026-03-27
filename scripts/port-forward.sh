#!/bin/bash

cd "$(dirname "$0")/.."

echo "Starting port forwarding..."
echo "Press Ctrl+C to stop"
echo ""

kubectl port-forward svc/vertica 5433:5433 -n streamflow