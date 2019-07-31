#!/bin/bash
if [ "$1" = "" ]; then
    echo "Please provide a valid argument {up, down}."
elif [ "$1" = "up" ]; then
    kubectl create -f https://raw.githubusercontent.com/MaZderMind/hostpath-provisioner/master/manifests/rbac.yaml
    kubectl create -f https://raw.githubusercontent.com/MaZderMind/hostpath-provisioner/master/manifests/storageclass.yaml
    kubectl create -f https://raw.githubusercontent.com/MaZderMind/hostpath-provisioner/master/manifests/deployment.yaml
elif [ "$1" = "down" ]; then
    kubectl delete -f https://raw.githubusercontent.com/MaZderMind/hostpath-provisioner/master/manifests/rbac.yaml
    kubectl delete -f https://raw.githubusercontent.com/MaZderMind/hostpath-provisioner/master/manifests/storageclass.yaml
    kubectl delete -f https://raw.githubusercontent.com/MaZderMind/hostpath-provisioner/master/manifests/deployment.yaml
else 
    echo "Please provide a valid argument {up, down}."
fi 