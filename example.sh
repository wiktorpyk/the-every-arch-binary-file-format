#!/bin/bash

echo ""

echo "Cleaning previous builds..."
make clean

echo ""

echo "Building all architectures and combining binaries..."
make

echo ""

echo "Extracting archives..."
python3 extract.py build_combined/main.ar.gz build_combined/libhello.so.ar.gz 

echo ""

echo "Running the main binary..."
./main

echo ""