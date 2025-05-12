#!/bin/bash

# Install Chromium dependencies
playwright install --with-deps chromium

# Run your script
python main.py
