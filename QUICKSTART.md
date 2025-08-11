# Collatz Binary Resonance Explorer - Quick Start

## Installation

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

## Quick Experiments

### 1. Discover Binary Patterns
```python
from analysis.binary_analyzer import CollatzBinaryAnalyzer

analyzer = CollatzBinaryAnalyzer()

# Analyze a specific number
result = analyzer.binary_analysis(27)
print(f"Resonance score: {result['resonance_score']}")

# Find patterns in a range
patterns = analyzer.find_binary_patterns(1, 1000)
```

### 2. Visualize Binary Evolution
```python
from visualizations.pattern_visualizer import BinaryPatternVisualizer

viz = BinaryPatternVisualizer()

# Create binary heatmap
viz.visualize_binary_trajectory(27)

# Generate resonance map
viz.create_resonance_map(1, 1000)
```

### 3. Run Advanced Experiments
```python
from experiments.advanced_experiments import ResonanceExperiments

exp = ResonanceExperiments()

# Shannon entropy analysis
entropy = exp.shannon_entropy_analysis(27)

# Fourier analysis of bit patterns
fourier = exp.fourier_bit_analysis(27, bit_position=0)

# Quantum-inspired model
quantum = exp.quantum_superposition_model(27)
```

## Key Insights

### Binary Operations in Collatz
- **Odd → Even**: 3n+1 always produces even (ends in 0)
- **Even → ?**: n/2 is a simple right shift
- **Pattern**: Odd numbers create complex bit interactions

### Resonance Phenomena
Numbers exhibit "resonance" when their binary patterns show:
- Periodic bit flips
- Repeating parity sequences  
- Harmonic relationships in bit positions

### Notable Discoveries
1. **Power-of-2 Attractors**: Many trajectories pass through 16, 64, 256
2. **Binary Palindromes**: Create unique trajectory signatures
3. **Entropy Decay**: Shannon entropy generally decreases toward convergence

## Research Directions

### Current Focus Areas
- [ ] Machine learning on binary features
- [ ] Fourier analysis of bit sequences
- [ ] Quantum circuit simulation
- [ ] Information-theoretic bounds

### Open Questions
1. Can binary resonance predict trajectory length?
2. Do certain bit patterns guarantee faster convergence?
3. Is there a binary "signature" for each equivalence class?

## Example: The Magic of 27

Number 27 (binary: 11011) has fascinating properties:
- Creates multiple binary palindromes in trajectory
- High resonance score (0.667)
- Trajectory length: 111 steps
- Maximum value: 9232 (binary: 10010000010000)

```python
# Explore 27's binary journey
analyzer = CollatzBinaryAnalyzer()
analysis = analyzer.binary_analysis(27)

# Key moments in 27's trajectory:
# Step 0: 11011 (27)
# Step 1: 1010010 (82) 
# Step 2: 101001 (41)
# ...
# Step 109: 10 (2)
# Step 110: 1 (1)
```

## Contributing

Found an interesting pattern? Have a hypothesis? 
Document your findings in the `experiments/` directory!

## References

- Collatz Conjecture (3n+1 problem)
- Binary representation theory
- Information theory & Shannon entropy
- Quantum computing principles
- Fourier analysis techniques
