#!/bin/bash

cd "$(dirname "$0")/.."

echo "Starting port forwarding..."
echo "Press Ctrl+C to stop"
echo ""

kubectl port-forward svc/vertica 5433:5433 -n streamflow &
echo "Vertica           → localhost:5433"

kubectl port-forward svc/kafka 9092:9092 -n streamflow &
echo "Kafka             → localhost:9092"

kubectl port-forward svc/kafka-ui 8080:8080 -n streamflow &
echo "Kafka UI          → localhost:8080"

kubectl port-forward svc/api-gateway 8000:8000 -n streamflow &
echo "API Gateway       → localhost:8000"

kubectl port-forward svc/auth-service 8001:8001 -n streamflow &
echo "Auth Service      → localhost:8001"

kubectl port-forward svc/ingestion-service 8002:8002 -n streamflow &
echo "Ingestion Service → localhost:8002"

kubectl port-forward svc/analytics-service 8003:8003 -n streamflow &
echo "Analytics Service → localhost:8003"

kubectl port-forward svc/alert-service 8004:8004 -n streamflow &
echo "Alert Service     → localhost:8004"

wait