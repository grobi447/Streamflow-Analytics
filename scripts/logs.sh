#!/bin/bash

cd "$(dirname "$0")/.."

if [ -z "$1" ]; then
  echo "Usage: ./scripts/logs.sh <service-name>"
  echo ""
  echo "Available services:"
  echo "  vertica"
  echo "  kafka"
  echo "  kafka-ui"
  echo "  ingestion-service"
else
  kubectl logs -l app=$1 -n streamflow --tail=100 -f
fi

read -p "Press Enter to exit..."