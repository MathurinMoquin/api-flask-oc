#!/bin/bash

new_version() {
    cp traefik/dynamic/green.yml traefik/dynamic/active.yml
    docker compose restart traefik
    echo "Switched to NEW version (V2)"
}

old_version() {
    cp traefik/dynamic/blue.yml traefik/dynamic/active.yml
    docker compose restart traefik
    echo "Switched to OLD version (V1)"
}

if [ -z "$1" ]; then
    echo "Usage: ./deployment.sh old|new"
    exit 1
fi

if [ "$1" = "old" ]; then
    old_version
elif [ "$1" = "new" ]; then
    new_version
else
    echo "Invalid argument: $1. Use 'old' or 'new'."
    exit 1
fi
