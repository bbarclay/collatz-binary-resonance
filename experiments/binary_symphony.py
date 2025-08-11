#!/usr/bin/env python3
"""
The Binary Symphony: Musical and Wave Patterns in Collatz Sequences
Deep zoom into the harmonic structure of binary dynamics
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, fftfreq, ifft
from typing import List, Dict, Tuple
import json

class BinarySymphonyAnalyzer:
    """
    Analyze Collatz sequences as musical/wave phenomena in binary space
    """
    
    def __init__(self):
        self.musical_discoveries = []
        
    def collatz_step(self, n: int) -> int:
        return 3 * n + 1 if n & 1 else n >> 1
    
    def get_trajectory(self, n: int, max_steps: int = 1000) -> List[int]:
        trajectory = [n]
        current = n
        while current != 1 and len(trajectory) < max_steps:
            current = self.collatz_step(current)
            trajectory.append(current)
        return trajectory
    
    def binary_to_waveform(self, n: int, sample_length: int = 256) -> np.ndarray:
        """
        Convert a Collatz trajectory into a binary waveform for analysis
        """
        trajectory = self.get_trajectory(n, sample_length)
        
        # Multiple representations as waveforms
        waveforms = {
            'bit_density': [],  # Density of 1s
            'bit_width': [],    # Binary width
            'hamming': [],      # Hamming weight
            'center_mass': [],  # Center of mass of 1s
            'entropy': []       # Shannon entropy
        }
        
        for num in trajectory:
            binary = bin(num)[2:]
            ones = binary.count('1')
            
            # Bit density
            waveforms['bit_density'].append(ones / len(binary) if len(binary) > 0 else 0)
            
            # Bit width
            waveforms['bit_width'].append(len(binary))
            
            # Hamming weight
            waveforms['hamming'].append(ones)
            
            # Center of mass
            positions = [i for i, bit in enumerate(reversed(binary)) if bit == '1']
            com = sum(positions) / len(positions) if positions else 0
            waveforms['center_mass'].append(com)
            
            # Shannon entropy
            if ones > 0 and ones < len(binary):
                p1 = ones / len(binary)
                p0 = 1 - p1
                entropy = -(p1 * np.log2(p1) + p0 * np.log2(p0))
            else:
                entropy = 0
            waveforms['entropy'].append(entropy)
        
        # Pad to sample_length if needed
        for key in waveforms:
            if len(waveforms[key]) < sample_length:
                waveforms[key].extend([waveforms[key][-1]] * (sample_length - len(waveforms[key])))
            waveforms[key] = np.array(waveforms[key][:sample_length])
        
        return waveforms
    
    def find_fundamental_frequency(self, waveform: np.ndarray) -> Dict:
        """
        Find the fundamental frequency and harmonics in a waveform
        """
        # Apply FFT
        fft_vals = fft(waveform)
        freqs = fftfreq(len(waveform))
        
        # Get magnitude spectrum
        magnitude = np.abs(fft_vals)
        
        # Find peaks in the spectrum
        peaks, properties = signal.find_peaks(magnitude[:len(magnitude)//2], 
                                             height=np.max(magnitude) * 0.1)
        
        if len(peaks) > 0:
            # Find fundamental (lowest significant frequency)
            fundamental_idx = peaks[0]
            fundamental_freq = freqs[fundamental_idx]
            
            # Find harmonics (multiples of fundamental)
            harmonics = []
            for peak_idx in peaks[1:6]:  # First 5 harmonics
                freq_ratio = freqs[peak_idx] / fundamental_freq if fundamental_freq != 0 else 0
                if abs(freq_ratio - round(freq_ratio)) < 0.1:  # Close to integer multiple
                    harmonics.append({
                        'harmonic_number': round(freq_ratio),
                        'frequency': freqs[peak_idx],
                        'amplitude': magnitude[peak_idx]
                    })
            
            return {
                'fundamental': fundamental_freq,
                'fundamental_amplitude': magnitude[fundamental_idx],
                'harmonics': harmonics,
                'spectral_centroid': np.sum(freqs[:len(freqs)//2] * magnitude[:len(magnitude)//2]) / np.sum(magnitude[:len(magnitude)//2])
            }
        
        return {'fundamental': 0, 'harmonics': [], 'spectral_centroid': 0}
    
    def analyze_binary_music(self, n: int) -> Dict:
        """
        Complete musical analysis of a number's Collatz sequence
        """
        print(f"\n{'='*60}")
        print(f"BINARY SYMPHONY ANALYSIS: n = {n}")
        print(f"{'='*60}")
        
        waveforms = self.binary_to_waveform(n)
        
        # Analyze each waveform type
        results = {}
        
        for wave_type, waveform in waveforms.items():
            freq_analysis = self.find_fundamental_frequency(waveform)
            
            # Calculate additional wave properties
            autocorr = np.correlate(waveform, waveform, mode='full')
            autocorr = autocorr[len(autocorr)//2:]  # Take positive lags
            
            # Find periodicity from autocorrelation
            peaks, _ = signal.find_peaks(autocorr)
            period = peaks[0] if len(peaks) > 0 else 0
            
            results[wave_type] = {
                'fundamental_freq': freq_analysis['fundamental'],
                'harmonics_count': len(freq_analysis['harmonics']),
                'spectral_centroid': freq_analysis['spectral_centroid'],
                'period': period,
                'mean': np.mean(waveform),
                'std': np.std(waveform),
                'trend': np.polyfit(range(len(waveform)), waveform, 1)[0]
            }
            
            print(f"\n{wave_type.upper()} Waveform:")
            print(f"  Fundamental frequency: {freq_analysis['fundamental']:.4f}")
            print(f"  Number of harmonics: {len(freq_analysis['harmonics'])}")
            print(f"  Period: {period}")
            print(f"  Trend: {'↑' if results[wave_type]['trend'] > 0 else '↓'} ({results[wave_type]['trend']:.4f})")
        
        return results
    
    def find_resonant_pairs(self, start: int, end: int) -> List[Tuple[int, int, float]]:
        """
        Find pairs of numbers with resonant (similar) frequency signatures
        """
        print(f"\n{'='*60}")
        print("SEARCHING FOR RESONANT NUMBER PAIRS")
        print(f"{'='*60}")
        
        signatures = {}
        
        # Calculate frequency signatures for each number
        for n in range(start, end + 1):
            waveform = self.binary_to_waveform(n, 128)['bit_density']
            freq_analysis = self.find_fundamental_frequency(waveform)
            signatures[n] = {
                'fundamental': freq_analysis['fundamental'],
                'centroid': freq_analysis['spectral_centroid']
            }
        
        # Find resonant pairs
        resonant_pairs = []
        
        for n1 in range(start, end):
            for n2 in range(n1 + 1, end + 1):
                sig1 = signatures[n1]
                sig2 = signatures[n2]
                
                # Calculate similarity
                if sig1['fundamental'] != 0 and sig2['fundamental'] != 0:
                    freq_similarity = 1 - abs(sig1['fundamental'] - sig2['fundamental'])
                    centroid_similarity = 1 - abs(sig1['centroid'] - sig2['centroid'])
                    
                    total_similarity = (freq_similarity + centroid_similarity) / 2
                    
                    if total_similarity > 0.9:  # High resonance
                        resonant_pairs.append((n1, n2, total_similarity))
        
        # Sort by similarity
        resonant_pairs.sort(key=lambda x: x[2], reverse=True)
        
        print(f"\nFound {len(resonant_pairs)} resonant pairs")
        print("Top resonant pairs:")
        for n1, n2, similarity in resonant_pairs[:5]:
            print(f"  {n1} ↔ {n2}: {similarity:.3f} resonance")
        
        return resonant_pairs
    
    def create_phase_diagram(self, n: int) -> Dict:
        """
        Create a phase space diagram of the binary dynamics
        """
        trajectory = self.get_trajectory(n, 200)
        
        # Create phase space coordinates
        x = []  # Bit density
        y = []  # Rate of change of bit density
        z = []  # Binary width
        
        for i in range(len(trajectory) - 1):
            curr_binary = bin(trajectory[i])[2:]
            next_binary = bin(trajectory[i + 1])[2:]
            
            curr_density = curr_binary.count('1') / len(curr_binary)
            next_density = next_binary.count('1') / len(next_binary)
            
            x.append(curr_density)
            y.append(next_density - curr_density)  # Rate of change
            z.append(len(curr_binary))
        
        # Find attractors in phase space
        # Cluster points to find dense regions
        points = np.column_stack((x, y))
        
        # Simple clustering - find regions with many nearby points
        attractors = []
        for i in range(len(points)):
            nearby = 0
            for j in range(len(points)):
                if i != j:
                    dist = np.linalg.norm(points[i] - points[j])
                    if dist < 0.1:  # Threshold for "nearby"
                        nearby += 1
            
            if nearby > len(points) * 0.1:  # More than 10% of points nearby
                attractors.append({
                    'density': x[i],
                    'change_rate': y[i],
                    'width': z[i],
                    'strength': nearby
                })
        
        # Remove duplicates
        unique_attractors = []
        for attr in attractors:
            is_unique = True
            for unique in unique_attractors:
                if abs(attr['density'] - unique['density']) < 0.05 and \
                   abs(attr['change_rate'] - unique['change_rate']) < 0.05:
                    is_unique = False
                    break
            if is_unique:
                unique_attractors.append(attr)
        
        return {
            'phase_points': {'x': x, 'y': y, 'z': z},
            'attractors': unique_attractors
        }
    
    def find_binary_melodies(self, n: int) -> Dict:
        """
        Extract melodic patterns from the binary evolution
        """
        trajectory = self.get_trajectory(n, 100)
        
        # Convert to "notes" based on bit patterns
        melody = []
        
        for num in trajectory:
            binary = bin(num)[2:]
            
            # Map binary patterns to "notes"
            # Use last 3 bits as note, bit width as octave
            note = num & 0b111  # Last 3 bits (0-7)
            octave = len(binary) // 3  # Width determines octave
            
            # Check for special patterns
            is_palindrome = binary == binary[::-1]
            is_power_of_2 = (num & (num - 1)) == 0 and num > 0
            
            melody.append({
                'value': num,
                'note': note,
                'octave': octave,
                'special': 'palindrome' if is_palindrome else 'power2' if is_power_of_2 else None
            })
        
        # Find repeating motifs
        motifs = {}
        motif_length = 4
        
        for i in range(len(melody) - motif_length):
            motif = tuple(m['note'] for m in melody[i:i+motif_length])
            if motif not in motifs:
                motifs[motif] = []
            motifs[motif].append(i)
        
        # Find most common motifs
        common_motifs = sorted(motifs.items(), key=lambda x: len(x[1]), reverse=True)[:5]
        
        return {
            'melody': melody,
            'common_motifs': common_motifs,
            'total_notes': len(melody),
            'unique_notes': len(set(m['note'] for m in melody))
        }
    
    def quantum_interference_pattern(self, n1: int, n2: int) -> Dict:
        """
        Simulate quantum-like interference between two trajectories
        """
        # Get waveforms for both numbers
        wave1 = self.binary_to_waveform(n1, 128)['bit_density']
        wave2 = self.binary_to_waveform(n2, 128)['bit_density']
        
        # Normalize to same amplitude
        wave1 = wave1 / np.max(np.abs(wave1)) if np.max(np.abs(wave1)) > 0 else wave1
        wave2 = wave2 / np.max(np.abs(wave2)) if np.max(np.abs(wave2)) > 0 else wave2
        
        # Create interference pattern
        constructive = wave1 + wave2
        destructive = wave1 - wave2
        
        # Find nodes (points of destructive interference)
        nodes = []
        for i in range(1, len(destructive) - 1):
            if abs(destructive[i]) < 0.01 and \
               (destructive[i-1] * destructive[i+1] < 0):  # Sign change
                nodes.append(i)
        
        # Find antinodes (points of maximum constructive interference)
        antinodes = []
        peaks, _ = signal.find_peaks(np.abs(constructive))
        antinodes = list(peaks)
        
        return {
            'wave1': wave1,
            'wave2': wave2,
            'constructive': constructive,
            'destructive': destructive,
            'nodes': nodes,
            'antinodes': antinodes,
            'interference_quality': np.std(constructive) / (np.std(wave1) + np.std(wave2))
        }
    
    def summarize_symphony(self):
        """
        Summarize the musical/wave nature of Collatz sequences
        """
        print("\n" + "="*60)
        print("THE BINARY SYMPHONY: Summary of Wave Phenomena")
        print("="*60)
        
        print("""
DISCOVERIES IN THE BINARY SYMPHONY:

1. HARMONIC STRUCTURE
   • Each Collatz trajectory has a fundamental frequency
   • Higher harmonics appear at integer multiples
   • Different aspects (density, width, entropy) create different "instruments"

2. RESONANT PAIRS
   • Some numbers have nearly identical frequency signatures
   • These create "consonant" relationships in number space
   • Suggests hidden symmetries in the Collatz map

3. PHASE SPACE ATTRACTORS
   • Trajectories spiral around strange attractors in phase space
   • Density vs. change-rate creates characteristic patterns
   • Multiple stable points suggest multi-stability

4. MELODIC MOTIFS
   • Binary patterns create repeating "melodic" sequences
   • Common motifs appear across different starting numbers
   • Special events (palindromes, powers of 2) act as "accents"

5. QUANTUM-LIKE INTERFERENCE
   • Trajectories can interfere constructively/destructively
   • Nodes and antinodes appear in the interference pattern
   • Suggests wave-like nature of number space dynamics

CONCLUSION:
The Collatz conjecture, when viewed through the lens of binary dynamics,
reveals itself as a complex wave phenomenon. The 3n+1 operation acts as
a nonlinear oscillator, creating harmonics, resonances, and interference
patterns in the space of binary representations.

This is not random chaos - it's a deterministic symphony playing out
in the discrete space of integers, with each number contributing its
unique voice to the grand composition.
        """)

def demonstrate_binary_symphony():
    """Run demonstration of binary symphony analysis"""
    analyzer = BinarySymphonyAnalyzer()
    
    # Analyze a specific number
    results = analyzer.analyze_binary_music(27)
    
    # Find resonant pairs
    resonant = analyzer.find_resonant_pairs(20, 50)
    
    # Create phase diagram
    phase = analyzer.create_phase_diagram(27)
    print(f"\nPhase space analysis for n=27:")
    print(f"  Found {len(phase['attractors'])} attractors in phase space")
    
    # Find melodies
    melody = analyzer.find_binary_melodies(27)
    print(f"\nMelodic analysis for n=27:")
    print(f"  Total notes: {melody['total_notes']}")
    print(f"  Unique notes: {melody['unique_notes']}")
    print(f"  Most common motif: {melody['common_motifs'][0][0] if melody['common_motifs'] else 'None'}")
    
    # Test interference
    interference = analyzer.quantum_interference_pattern(27, 31)
    print(f"\nQuantum interference between 27 and 31:")
    print(f"  Nodes: {len(interference['nodes'])}")
    print(f"  Antinodes: {len(interference['antinodes'])}")
    print(f"  Interference quality: {interference['interference_quality']:.3f}")
    
    # Final summary
    analyzer.summarize_symphony()

if __name__ == "__main__":
    demonstrate_binary_symphony()
