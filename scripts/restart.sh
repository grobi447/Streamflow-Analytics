#!/bin/bash

cd "$(dirname "$0")/.."

echo "Restarting all deployments..."
kubectl rollout restart deployment/vertica -n streamflow
kubectl rollout restart deployment/kafka -n streamflow
kubectl rollout restart deployment/kafka-ui -n streamflow
kubectl rollout restart deployment/nginx -n streamflow
kubectl rollout restart deployment/simulator -n streamflow
kubectl rollout restart deployment/auth-service -n streamflow
kubectl rollout restart deployment/ingestion-service -n streamflow
kubectl rollout restart deployment/analytics-service -n streamflow
kubectl rollout restart deployment/alert-service -n streamflow
kubectl rollout restart deployment/api-gateway -n streamflow
kubectl rollout restart deployment/frontend -n streamflow
echo "Done!"

read -p "Press Enter to exit..."