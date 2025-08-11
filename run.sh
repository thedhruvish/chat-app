#!/bin/bash

# install uv 
pip install uv
echo "Installing uv"
# Create a virtual environment 

echo "Syncing uv"
uv sync


echo "Running uv"
fastapi run app/app.py