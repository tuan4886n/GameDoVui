#!/bin/bash
echo "🌀 Port-forward flask API (Ingress) ..."
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8888:80