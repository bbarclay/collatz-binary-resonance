#!/usr/bin/env python3
"""
Advanced Binary Resonance Experiments
Exploring quantum-inspired and information-theoretic approaches to Collatz
"""

import numpy as np
from scipy import signal, stats
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis.binary_analyzer import CollatzBinaryAnalyzer

class ResonanceExperiments:
    def __init__(self):
        self.analyzer = CollatzBinaryAnalyzer()
    
    def shannon_entropy_analysis(self, n: int) -> Dict:
        """
        Calculate Shannon entropy evolution through trajectory
        Lower entropy suggests more predictable patterns
        """
        trajectory = self.analyzer.get_trajectory(n)
        entropies = []
        
        for num in trajectory:
            binary = bin(num)[2:]
            if len(binary) > 1:
                # Calculate probability of 0s and 1s
                p1 = binary.count('1') / len(binary)
                p0 = 1 - p1
                
                # Shannon entropy
                entropy = 0
                if p0 > 0:
                    entropy -= p0 * np.log2(p0)
                if p1 > 0:
                    entropy -= p1 * np.log2(p1)
                entropies.append(entropy)
            else:
                entropies.append(0)
        
        return {
            'number': n,
            'entropies': entropies,
            'mean_entropy': np.mean(entropies),
            'entropy_variance': np.var(entropies),
            'entropy_trend': np.polyfit(range(len(entropies)), entropies, 1)[0] if len(entropies) > 1 else 0
        }
    
    def fourier_bit_analysis(self, n: int, bit_position: int = 0) -> Dict:
        """
        Apply Fourier transform to bit position time series
        Identifies periodic components in bit behavior
        """
        trajectory = self.analyzer.get_trajectory(n)[:100]  # Limit for FFT
        
        # Extract bit values at specific position
        bit_series = []
        for num in trajectory:
            binary = bin(num)[2:].zfill(32)  # Pad to 32 bits
            if bit_position < len(binary):
                bit_series.append(int(binary[-(bit_position+1)]))  # LSB = position 0
            else:
                bit_series.append(0)
        
        if len(bit_series) < 4:
            return {'error': 'Trajectory too short for FFT'}
        
        # Apply FFT
        fft_vals = fft(bit_series)
        freqs = fftfreq(len(bit_series))
        
        # Find dominant frequencies
        power_spectrum = np.abs(fft_vals) ** 2
        dominant_freq_idx = np.argsort(power_spectrum)[-5:]  # Top 5 frequencies
        
        return {
            'number': n,
            'bit_position': bit_position,
            'dominant_frequencies': freqs[dominant_freq_idx].tolist(),
            'power_spectrum': power_spectrum.tolist(),
            'periodicity_score': np.max(power_spectrum[1:]) / np.mean(power_spectrum) if len(power_spectrum) > 1 else 0
        }
    
    def quantum_superposition_model(self, n: int) -> Dict:
        """
        Model Collatz trajectory as quantum-like superposition of binary states
        Each step involves 'measurement' that collapses to specific state
        """
        trajectory = self.analyzer.get_trajectory(n)
        
        # Initialize quantum-like state vector
        max_bits = max(x.bit_length() for x in trajectory[:20])
        
        states = []
        for num in trajectory[:20]:  # Limit for computational efficiency
            # Create state vector (amplitudes for each bit)
            binary = bin(num)[2:].zfill(max_bits)
            state = np.array([complex(int(b)) for b in binary])
            
            # Normalize (quantum state normalization)
            norm = np.sqrt(np.sum(np.abs(state) ** 2))
            if norm > 0:
                state = state / norm
            
            states.append(state)
        
        # Calculate "quantum" metrics
        coherence_scores = []
        for i in range(len(states) - 1):
            # Overlap between consecutive states (fidelity)
            overlap = np.abs(np.vdot(states[i], states[i+1])) ** 2
            coherence_scores.append(overlap)
        
        # Entanglement-like measure (correlation between bit positions)
        if len(states) > 2:
            bit_correlations = np.zeros((max_bits, max_bits))
            for state in states:
                for i in range(max_bits):
                    for j in range(i+1, max_bits):
                        bit_correlations[i, j] += np.abs(state[i] * np.conj(state[j]))
            bit_correlations /= len(states)
        else:
            bit_correlations = None
        
        return {
            'number': n,
            'avg_coherence': np.mean(coherence_scores) if coherence_scores else 0,
            'coherence_variance': np.var(coherence_scores) if coherence_scores else 0,
            'max_entanglement': np.max(bit_correlations) if bit_correlations is not None else 0,
            'quantum_dimension': max_bits
        }
    
    def binary_attractor_analysis(self, sample_size: int = 1000) -> Dict:
        """
        Analyze if certain binary patterns act as attractors
        """
        attractor_candidates = {}
        
        for n in range(1, sample_size + 1):
            trajectory = self.analyzer.get_trajectory(n)
            
            for num in trajectory:
                binary = bin(num)[2:]
                
                # Check for special patterns
                if binary == binary[::-1] and len(binary) > 1:  # Palindrome
                    key = f"palindrome_{binary}"
                    if key not in attractor_candidates:
                        attractor_candidates[key] = {'count': 0, 'sources': []}
                    attractor_candidates[key]['count'] += 1
                    attractor_candidates[key]['sources'].append(n)
                
                if binary.count('1') == 1:  # Power of 2
                    key = f"power_of_2_{num}"
                    if key not in attractor_candidates:
                        attractor_candidates[key] = {'count': 0, 'sources': []}
                    attractor_candidates[key]['count'] += 1
                    attractor_candidates[key]['sources'].append(n)
                
                if '111' in binary:  # Three consecutive 1s
                    key = "triple_ones"
                    if key not in attractor_candidates:
                        attractor_candidates[key] = {'count': 0, 'sources': []}
                    attractor_candidates[key]['count'] += 1
                    attractor_candidates[key]['sources'].append(n)
        
        # Sort by frequency
        sorted_attractors = sorted(attractor_candidates.items(), 
                                 key=lambda x: x[1]['count'], 
                                 reverse=True)
        
        return {
            'top_attractors': sorted_attractors[:10],
            'total_patterns_found': len(attractor_candidates),
            'most_common_pattern': sorted_attractors[0] if sorted_attractors else None
        }
    
    def run_comprehensive_experiment(self, n: int):
        """Run all experiments on a single number and create comprehensive report"""
        print(f"\n{'='*60}")
        print(f"COMPREHENSIVE BINARY RESONANCE ANALYSIS FOR n = {n}")
        print(f"{'='*60}")
        
        # Basic analysis
        basic = self.analyzer.binary_analysis(n)
        print(f"\nBasic Properties:")
        print(f"  Binary: {basic['start_binary']}")
        print(f"  Trajectory length: {basic['trajectory_length']}")
        print(f"  Resonance score: {basic['resonance_score']:.4f}")
        
        # Shannon entropy
        entropy = self.shannon_entropy_analysis(n)
        print(f"\nShannon Entropy Analysis:")
        print(f"  Mean entropy: {entropy['mean_entropy']:.4f}")
        print(f"  Entropy trend: {'decreasing' if entropy['entropy_trend'] < 0 else 'increasing'}")
        print(f"  Entropy variance: {entropy['entropy_variance']:.4f}")
        
        # Fourier analysis
        fourier = self.fourier_bit_analysis(n, bit_position=0)
        print(f"\nFourier Analysis (LSB):")
        print(f"  Periodicity score: {fourier.get('periodicity_score', 0):.4f}")
        if 'dominant_frequencies' in fourier:
            print(f"  Dominant frequencies: {fourier['dominant_frequencies'][:3]}")
        
        # Quantum model
        quantum = self.quantum_superposition_model(n)
        print(f"\nQuantum-Inspired Model:")
        print(f"  Average coherence: {quantum['avg_coherence']:.4f}")
        print(f"  Max entanglement: {quantum['max_entanglement']:.4f}")
        print(f"  Quantum dimension: {quantum['quantum_dimension']}")
        
        # Visualization
        self.visualize_experiment_results(n, entropy, fourier)
    
    def visualize_experiment_results(self, n: int, entropy_data: Dict, fourier_data: Dict):
        """Create visualization of experimental results"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Entropy evolution
        axes[0, 0].plot(entropy_data['entropies'], 'b-', linewidth=2, alpha=0.7)
        axes[0, 0].axhline(y=entropy_data['mean_entropy'], color='r', 
                          linestyle='--', label=f"Mean: {entropy_data['mean_entropy']:.3f}")
        axes[0, 0].set_xlabel('Trajectory Step')
        axes[0, 0].set_ylabel('Shannon Entropy')
        axes[0, 0].set_title(f'Entropy Evolution for n={n}')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Binary width evolution
        trajectory = self.analyzer.get_trajectory(n)[:50]
        bit_lengths = [x.bit_length() for x in trajectory]
        axes[0, 1].plot(bit_lengths, 'g-', linewidth=2, alpha=0.7)
        axes[0, 1].fill_between(range(len(bit_lengths)), bit_lengths, alpha=0.3, color='green')
        axes[0, 1].set_xlabel('Trajectory Step')
        axes[0, 1].set_ylabel('Binary Width (bits)')
        axes[0, 1].set_title('Binary Width Evolution')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Hamming weight evolution
        hamming_weights = [bin(x).count('1') for x in trajectory]
        axes[1, 0].bar(range(len(hamming_weights)), hamming_weights, 
                      color='purple', alpha=0.6)
        axes[1, 0].set_xlabel('Trajectory Step')
        axes[1, 0].set_ylabel('Hamming Weight')
        axes[1, 0].set_title('Hamming Weight (Number of 1s)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Power spectrum from Fourier analysis
        if 'power_spectrum' in fourier_data:
            power_spectrum = fourier_data['power_spectrum'][:20]  # First 20 frequencies
            axes[1, 1].stem(range(len(power_spectrum)), power_spectrum, basefmt=' ')
            axes[1, 1].set_xlabel('Frequency Component')
            axes[1, 1].set_ylabel('Power')
            axes[1, 1].set_title(f'Bit Position Power Spectrum (Position {fourier_data["bit_position"]})')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle(f'Binary Resonance Experimental Results for n={n}')
        plt.tight_layout()
        plt.show()

def main():
    """Run demonstration experiments"""
    experiments = ResonanceExperiments()
    
    # Test on some interesting numbers
    test_numbers = [27, 31, 127, 255, 837799]  # Including the famous 837799
    
    for n in test_numbers[:3]:  # Limit for demonstration
        experiments.run_comprehensive_experiment(n)
    
    # Attractor analysis
    print(f"\n{'='*60}")
    print("BINARY ATTRACTOR ANALYSIS (n ∈ [1, 500])")
    print(f"{'='*60}")
    
    attractors = experiments.binary_attractor_analysis(sample_size=500)
    print(f"\nTop Binary Attractors:")
    for pattern, data in attractors['top_attractors'][:5]:
        print(f"  {pattern}: encountered {data['count']} times")
        print(f"    Example sources: {data['sources'][:5]}")

if __name__ == "__main__":
    main()
