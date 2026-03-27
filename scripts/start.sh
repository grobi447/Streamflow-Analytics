#!/bin/bash
cd "$(dirname "$0")/.."

echo "Starting StreamFlow Analytics..."

kubectl apply -f k8s/namespace.yaml

if [ -f "k8s/secrets/vertica-secret.yaml" ]; then
  kubectl apply -f k8s/secrets/vertica-secret.yaml
else
  echo "Warning: k8s/secrets/vertica-secret.yaml not found!"
  echo "Create it manually before starting."
fi

kubectl apply -f k8s/vertica/

echo ""
echo "Waiting for Vertica to be ready..."
kubectl wait --for=condition=ready pod -l app=vertica -n streamflow --timeout=120s
echo "Done!"

read -p "Press Enter to exit..."