#!/bin/bash

echo "StreamFlow Analytics Status"
echo "================================"
echo ""
echo "Pods:"
kubectl get pods -n streamflow
echo ""
echo "Services:"
kubectl get svc -n streamflow
echo ""
echo "Deployments:"
kubectl get deployments -n streamflow

read -p "Press Enter to exit..."