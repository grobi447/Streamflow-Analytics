#!/bin/bash

cd "$(dirname "$0")/.."

if [ -z "$1" ]; then
  echo "Usage: ./scripts/logs.sh <service-name>"
  echo ""
  echo "Available services:"
  echo "  vertica"
  echo "  kafka"
  echo "  kafka-ui"
  echo "  nginx"
  echo "  simulator"
  echo "  api-gateway"
  echo "  auth-service"
  echo "  ingestion-service"
  echo "  analytics-service"
  echo "  alert-service"
  echo "  frontend"
else
  kubectl logs -l app=$1 -n streamflow --tail=100 -f
fi