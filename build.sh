#!/usr/bin/env bash
# Render Build Script
set -o errexit

echo "==> Upgrading pip..."
python3 -m pip install --upgrade pip

echo "==> Installing requirements..."
pip install -r requirements.txt

echo "==> Build finished."
