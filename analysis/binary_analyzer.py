#!/usr/bin/env python3
"""
Collatz Binary Resonance Analyzer
Explores the relationship between binary representations and Collatz trajectories
"""

import numpy as np
from typing import List, Tuple, Dict
from collections import defaultdict
import json

class CollatzBinaryAnalyzer:
    def __init__(self):
        self.trajectory_cache = {}
        self.pattern_database = defaultdict(list)
        
    def collatz_step(self, n: int) -> int:
        """Single Collatz step with binary insight"""
        if n & 1:  # Check last bit for odd/even
            return 3 * n + 1
        else:
            return n >> 1  # Right shift for division by 2
    
    def get_trajectory(self, n: int) -> List[int]:
        """Generate full Collatz trajectory"""
        if n in self.trajectory_cache:
            return self.trajectory_cache[n]
        
        trajectory = [n]
        current = n
        while current != 1:
            current = self.collatz_step(current)
            trajectory.append(current)
            if current in self.trajectory_cache:
                # Use cached partial trajectory
                trajectory.extend(self.trajectory_cache[current][1:])
                break
        
        self.trajectory_cache[n] = trajectory
        return trajectory
    
    def binary_analysis(self, n: int) -> Dict:
        """Comprehensive binary analysis of a number's Collatz trajectory"""
        trajectory = self.get_trajectory(n)
        
        analysis = {
            'start': n,
            'start_binary': bin(n)[2:],
            'trajectory_length': len(trajectory),
            'binary_trajectory': [bin(x)[2:] for x in trajectory],
            'bit_lengths': [len(bin(x)[2:]) for x in trajectory],
            'bit_transitions': [],
            'hamming_weights': [bin(x).count('1') for x in trajectory],
            'resonance_score': 0
        }
        
        # Analyze bit transitions
        for i in range(len(trajectory) - 1):
            curr_bits = bin(trajectory[i])[2:].zfill(64)
            next_bits = bin(trajectory[i+1])[2:].zfill(64)
            
            transition = {
                'step': i,
                'operation': '3n+1' if trajectory[i] & 1 else 'n/2',
                'bits_changed': sum(c != n for c, n in zip(curr_bits, next_bits)),
                'bit_diff': trajectory[i+1].bit_length() - trajectory[i].bit_length()
            }
            analysis['bit_transitions'].append(transition)
        
        # Calculate resonance score based on bit pattern periodicity
        analysis['resonance_score'] = self._calculate_resonance(trajectory)
        
        return analysis
    
    def _calculate_resonance(self, trajectory: List[int]) -> float:
        """
        Calculate a resonance score based on repeating binary patterns.
        Higher scores indicate more regular/resonant behavior.
        """
        if len(trajectory) < 3:
            return 0.0
        
        # Look for repeating patterns in bit parity sequence
        parity_sequence = [x & 1 for x in trajectory]
        
        # Find repeating subsequences
        pattern_scores = []
        for pattern_len in range(2, min(len(parity_sequence) // 2, 10)):
            matches = 0
            for i in range(len(parity_sequence) - pattern_len):
                if parity_sequence[i:i+pattern_len] == parity_sequence[i+pattern_len:i+2*pattern_len]:
                    matches += 1
            if matches > 0:
                pattern_scores.append(matches * pattern_len)
        
        return sum(pattern_scores) / len(trajectory) if pattern_scores else 0.0
    
    def find_binary_patterns(self, start: int, end: int) -> Dict:
        """Discover interesting binary patterns in a range"""
        patterns = {
            'palindromic_trajectories': [],
            'power_of_2_encounters': defaultdict(int),
            'high_resonance': [],
            'bit_length_sequences': defaultdict(list)
        }
        
        for n in range(start, end + 1):
            analysis = self.binary_analysis(n)
            
            # Check for palindromic binary at any point
            for i, binary_str in enumerate(analysis['binary_trajectory']):
                if binary_str == binary_str[::-1] and len(binary_str) > 1:
                    patterns['palindromic_trajectories'].append({
                        'number': n,
                        'step': i,
                        'palindrome': binary_str
                    })
            
            # Count power of 2 encounters
            for num in self.get_trajectory(n):
                if num & (num - 1) == 0 and num > 1:  # Check if power of 2
                    patterns['power_of_2_encounters'][num] += 1
            
            # Track high resonance scores
            if analysis['resonance_score'] > 0.5:
                patterns['high_resonance'].append({
                    'number': n,
                    'score': analysis['resonance_score'],
                    'length': analysis['trajectory_length']
                })
            
            # Collect bit length sequences for pattern analysis
            bit_seq_key = tuple(analysis['bit_lengths'][:10])  # First 10 bit lengths
            patterns['bit_length_sequences'][bit_seq_key].append(n)
        
        return patterns
    
    def export_analysis(self, n: int, filename: str):
        """Export detailed analysis to JSON file"""
        analysis = self.binary_analysis(n)
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"Analysis exported to {filename}")

def demonstrate_binary_resonance():
    """Demonstrate key findings about binary patterns in Collatz sequences"""
    analyzer = CollatzBinaryAnalyzer()
    
    print("=" * 60)
    print("COLLATZ BINARY RESONANCE EXPLORER")
    print("=" * 60)
    
    # Example 1: Analyze a specific number
    n = 27  # Interesting trajectory
    print(f"\nDetailed analysis of n = {n}:")
    analysis = analyzer.binary_analysis(n)
    print(f"Binary: {analysis['start_binary']}")
    print(f"Trajectory length: {analysis['trajectory_length']}")
    print(f"Resonance score: {analysis['resonance_score']:.3f}")
    print(f"Bit length progression: {analysis['bit_lengths'][:10]}...")
    
    # Example 2: Find patterns in a range
    print("\nSearching for patterns in range [1, 100]...")
    patterns = analyzer.find_binary_patterns(1, 100)
    
    print(f"\nFound {len(patterns['palindromic_trajectories'])} palindromic encounters")
    if patterns['palindromic_trajectories']:
        example = patterns['palindromic_trajectories'][0]
        print(f"  Example: n={example['number']} creates palindrome '{example['palindrome']}' at step {example['step']}")
    
    print(f"\nHigh resonance numbers (score > 0.5):")
    for item in sorted(patterns['high_resonance'], key=lambda x: x['score'], reverse=True)[:5]:
        print(f"  n={item['number']}: score={item['score']:.3f}, length={item['length']}")
    
    print(f"\nMost common power-of-2 encounters:")
    for power, count in sorted(patterns['power_of_2_encounters'].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {power} ({bin(power)}): encountered {count} times")
    
    # Example 3: Binary insight
    print("\n" + "=" * 60)
    print("BINARY INSIGHT: Why 3n+1 creates specific patterns")
    print("=" * 60)
    
    n = 5  # Simple example
    print(f"\nTracing n = {n}:")
    current = n
    for step in range(6):
        binary = bin(current)[2:]
        if current & 1:  # Odd
            next_val = 3 * current + 1
            operation = f"3*{current}+1"
            print(f"  {current:4d} = {binary:>8s} (odd)  -> {operation:>10s} = {next_val}")
        else:
            next_val = current >> 1
            operation = f"{current}/2"
            print(f"  {current:4d} = {binary:>8s} (even) -> {operation:>10s} = {next_val}")
        current = next_val
        if current == 1:
            print(f"  {current:4d} = {bin(current)[2:]:>8s} (reached 1)")
            break

if __name__ == "__main__":
    demonstrate_binary_resonance()
