#!/bin/bash

cd "$(dirname "$0")/.."

echo "Building ingestion-service..."
docker build -t streamflow/ingestion-service:latest ./backend/ingestion-service
docker tag streamflow/ingestion-service:latest localhost/streamflow/ingestion-service:latest
echo "Done!"

read -p "Press Enter to exit..."