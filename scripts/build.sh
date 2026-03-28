#!/bin/bash

cd "$(dirname "$0")/.."

echo "Building ingestion-service..."
docker build -t streamflow/ingestion-service:latest ./backend/ingestion-service
docker tag streamflow/ingestion-service:latest localhost/streamflow/ingestion-service:latest
echo "Done!"

echo "Building analytics-service..."
docker build -t streamflow/analytics-service:latest ./backend/analytics-service
docker tag streamflow/analytics-service:latest localhost/streamflow/analytics-service:latest
echo "Done!"

read -p "Press Enter to exit..."