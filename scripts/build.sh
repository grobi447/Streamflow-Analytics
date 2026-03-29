#!/bin/bash

cd "$(dirname "$0")/.."

echo "Building simulator..."
docker build -t streamflow/simulator:latest ./simulator
docker tag streamflow/simulator:latest localhost/streamflow/simulator:latest
echo "Done!"

echo "Building ingestion-service..."
docker build -t streamflow/ingestion-service:latest ./backend/ingestion-service
docker tag streamflow/ingestion-service:latest localhost/streamflow/ingestion-service:latest
echo "Done!"

echo "Building analytics-service..."
docker build -t streamflow/analytics-service:latest ./backend/analytics-service
docker tag streamflow/analytics-service:latest localhost/streamflow/analytics-service:latest
echo "Done!"

echo "Building alert-service..."
docker build -t streamflow/alert-service:latest ./backend/alert-service
docker tag streamflow/alert-service:latest localhost/streamflow/alert-service:latest
echo "Done!"

echo "Building auth-service..."
docker build -t streamflow/auth-service:latest ./backend/auth-service
docker tag streamflow/auth-service:latest localhost/streamflow/auth-service:latest
echo "Done!"

echo "Building api-gateway..."
docker build -t streamflow/api-gateway:latest ./backend/api-gateway
docker tag streamflow/api-gateway:latest localhost/streamflow/api-gateway:latest
echo "Done!"

echo "Building frontend..."
docker build -t streamflow/frontend:latest ./frontend
docker tag streamflow/frontend:latest localhost/streamflow/frontend:latest
echo "Done!"

echo "All images built!"

read -p "Press Enter to exit..."