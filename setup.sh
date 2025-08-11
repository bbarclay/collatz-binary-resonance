#!/bin/bash

# Setup script for Collatz Binary Resonance project

echo "Setting up Collatz Binary Resonance Explorer..."

# Create virtual environment (optional but recommended)
if command -v python3 &>/dev/null; then
    echo "Python 3 found. Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    # Install required packages
    echo "Installing required packages..."
    pip install numpy matplotlib seaborn scipy
    
    echo "Setup complete! To run the demonstrations:"
    echo "  1. Basic analysis: python analysis/binary_analyzer.py"
    echo "  2. Visualizations: python visualizations/pattern_visualizer.py"
    echo "  3. Advanced experiments: python experiments/advanced_experiments.py"
else
    echo "Python 3 not found. Please install Python 3 to continue."
    exit 1
fi

# Create data directory for outputs
mkdir -p data
mkdir -p outputs

echo ""
echo "Project structure created successfully!"
echo "Explore the binary patterns hiding in the Collatz conjecture!"
