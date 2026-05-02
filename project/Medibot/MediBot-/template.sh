#!/bin/bash

echo "Setting up Offline Medical Chatbot..."

# Create folders
mkdir -p src
mkdir -p data
mkdir -p templates
mkdir -p static
mkdir -p models

# Create files
touch app.py
touch store_index.py
touch src/helper.py
touch templates/index.html
touch .env
touch requirements.txt

echo "Structure ready ✅"