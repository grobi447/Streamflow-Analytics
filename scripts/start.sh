#!/bin/bash

cd "$(dirname "$0")/.."

echo "Starting StreamFlow Analytics..."

kubectl apply -f k8s/namespace.yaml

if [ -f "k8s/secrets/vertica-secret.yaml" ]; then
  kubectl apply -f k8s/secrets/vertica-secret.yaml
else
  echo "Warning: k8s/secrets/vertica-secret.yaml not found!"
fi

if [ -f "k8s/secrets/auth-secret.yaml" ]; then
  kubectl apply -f k8s/secrets/auth-secret.yaml
else
  echo "Warning: k8s/secrets/auth-secret.yaml not found!"
fi

kubectl apply -f k8s/vertica/
kubectl apply -f k8s/kafka/
kubectl apply -f k8s/microservices/ingestion-service/
kubectl apply -f k8s/microservices/analytics-service/
kubectl apply -f k8s/microservices/alert-service/
kubectl apply -f k8s/microservices/auth-service/
kubectl apply -f k8s/microservices/api-gateway/

echo ""
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=vertica -n streamflow --timeout=120s
kubectl wait --for=condition=ready pod -l app=kafka -n streamflow --timeout=120s
kubectl wait --for=condition=ready pod -l app=ingestion-service -n streamflow --timeout=120s
kubectl wait --for=condition=ready pod -l app=analytics-service -n streamflow --timeout=120s
kubectl wait --for=condition=ready pod -l app=alert-service -n streamflow --timeout=120s
kubectl wait --for=condition=ready pod -l app=auth-service -n streamflow --timeout=120s
kubectl wait --for=condition=ready pod -l app=api-gateway -n streamflow --timeout=120s
echo "Done!"

read -p "Press Enter to exit..."