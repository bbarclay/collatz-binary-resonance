#!/usr/bin/env python3
"""
Binary Pattern Visualizer for Collatz Sequences
Creates visual representations of binary patterns in Collatz trajectories
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from typing import List, Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis.binary_analyzer import CollatzBinaryAnalyzer

class BinaryPatternVisualizer:
    def __init__(self):
        self.analyzer = CollatzBinaryAnalyzer()
        # Custom colormap for binary visualization
        self.binary_cmap = LinearSegmentedColormap.from_list(
            'binary', ['#000428', '#004e92', '#00a8cc', '#ffa400', '#ffaa00']
        )
        
    def visualize_binary_trajectory(self, n: int, max_steps: int = 50):
        """Create a heatmap of binary representations through trajectory"""
        trajectory = self.analyzer.get_trajectory(n)[:max_steps]
        
        # Prepare binary matrix
        max_bits = max(x.bit_length() for x in trajectory)
        binary_matrix = np.zeros((len(trajectory), max_bits))
        
        for i, num in enumerate(trajectory):
            binary_str = bin(num)[2:].zfill(max_bits)
            for j, bit in enumerate(binary_str):
                binary_matrix[i, j] = int(bit)
        
        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
        
        # Binary heatmap
        im = ax1.imshow(binary_matrix, cmap='YlOrRd', aspect='auto')
        ax1.set_xlabel('Bit Position (MSB to LSB)')
        ax1.set_ylabel('Trajectory Step')
        ax1.set_title(f'Binary Evolution of n={n}')
        
        # Add trajectory values on the side
        for i in range(min(len(trajectory), 20)):
            ax1.text(-1, i, str(trajectory[i]), ha='right', va='center', fontsize=8)
        
        # Bit frequency analysis
        bit_frequencies = binary_matrix.mean(axis=0)
        ax2.bar(range(max_bits), bit_frequencies, color='steelblue', alpha=0.7)
        ax2.set_xlabel('Bit Position')
        ax2.set_ylabel('Frequency of 1s')
        ax2.set_title('Bit Position Activity')
        ax2.grid(True, alpha=0.3)
        
        plt.colorbar(im, ax=ax1, label='Bit Value')
        plt.suptitle(f'Binary Pattern Analysis for Collatz Sequence starting at {n}')
        plt.tight_layout()
        return fig
    
    def create_resonance_map(self, start: int, end: int, sample_size: int = 100):
        """Create a 2D resonance map showing pattern strength"""
        # Sample numbers for analysis
        numbers = np.linspace(start, end, sample_size, dtype=int)
        
        # Calculate features for each number
        features = []
        for n in numbers:
            analysis = self.analyzer.binary_analysis(n)
            features.append([
                analysis['trajectory_length'],
                analysis['resonance_score'],
                max(analysis['hamming_weights']),
                np.mean(analysis['hamming_weights'])
            ])
        
        features = np.array(features)
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Trajectory length distribution
        axes[0, 0].hist(features[:, 0], bins=30, color='teal', alpha=0.7, edgecolor='black')
        axes[0, 0].set_xlabel('Trajectory Length')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Distribution of Trajectory Lengths')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Resonance score vs trajectory length
        scatter = axes[0, 1].scatter(features[:, 0], features[:, 1], 
                                    c=features[:, 2], cmap='viridis', 
                                    alpha=0.6, s=50)
        axes[0, 1].set_xlabel('Trajectory Length')
        axes[0, 1].set_ylabel('Resonance Score')
        axes[0, 1].set_title('Resonance vs Trajectory Length')
        plt.colorbar(scatter, ax=axes[0, 1], label='Max Hamming Weight')
        
        # Hamming weight evolution
        axes[1, 0].scatter(features[:, 2], features[:, 3], 
                          c=features[:, 1], cmap='coolwarm', 
                          alpha=0.6, s=50)
        axes[1, 0].set_xlabel('Max Hamming Weight')
        axes[1, 0].set_ylabel('Mean Hamming Weight')
        axes[1, 0].set_title('Hamming Weight Characteristics')
        
        # 2D histogram of resonance patterns
        h = axes[1, 1].hist2d(features[:, 0], features[:, 1], 
                              bins=[20, 20], cmap='YlOrRd')
        axes[1, 1].set_xlabel('Trajectory Length')
        axes[1, 1].set_ylabel('Resonance Score')
        axes[1, 1].set_title('Density Map of Resonance Patterns')
        plt.colorbar(h[3], ax=axes[1, 1], label='Count')
        
        plt.suptitle(f'Collatz Binary Resonance Map (n ∈ [{start}, {end}])')
        plt.tight_layout()
        return fig
    
    def visualize_bit_transitions(self, n: int):
        """Visualize how bits change through the trajectory"""
        analysis = self.analyzer.binary_analysis(n)
        trajectory = self.analyzer.get_trajectory(n)[:30]  # Limit for visibility
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Bit transition diagram
        max_bits = max(x.bit_length() for x in trajectory)
        
        for i in range(len(trajectory) - 1):
            curr_bits = bin(trajectory[i])[2:].zfill(max_bits)
            next_bits = bin(trajectory[i+1])[2:].zfill(max_bits)
            
            for j, (cb, nb) in enumerate(zip(curr_bits, next_bits)):
                if cb != nb:
                    # Bit changed
                    color = 'red' if cb == '1' else 'green'
                    ax1.arrow(i, j, 0.8, 0, head_width=0.3, head_length=0.1,
                             fc=color, ec=color, alpha=0.5)
                
                # Draw the bits
                color = 'black' if cb == '1' else 'lightgray'
                ax1.add_patch(patches.Rectangle((i-0.4, j-0.4), 0.8, 0.8,
                                               facecolor=color, alpha=0.7))
        
        ax1.set_xlim(-1, len(trajectory))
        ax1.set_ylim(-1, max_bits)
        ax1.set_xlabel('Trajectory Step')
        ax1.set_ylabel('Bit Position')
        ax1.set_title(f'Bit Transition Diagram for n={n}')
        ax1.invert_yaxis()
        
        # Transition frequency by operation type
        transitions = analysis['bit_transitions'][:29]
        odd_changes = [t['bits_changed'] for t in transitions if t['operation'] == '3n+1']
        even_changes = [t['bits_changed'] for t in transitions if t['operation'] == 'n/2']
        
        x = np.arange(max(len(odd_changes), len(even_changes)))
        width = 0.35
        
        if odd_changes:
            ax2.bar(x[:len(odd_changes)] - width/2, odd_changes, width, 
                   label='3n+1 (odd)', color='coral', alpha=0.7)
        if even_changes:
            ax2.bar(x[:len(even_changes)] + width/2, even_changes, width,
                   label='n/2 (even)', color='skyblue', alpha=0.7)
        
        ax2.set_xlabel('Operation Index')
        ax2.set_ylabel('Number of Bits Changed')
        ax2.set_title('Bit Changes by Operation Type')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_binary_spiral(self, n: int, max_steps: int = 100):
        """Create a spiral visualization of binary evolution"""
        trajectory = self.analyzer.get_trajectory(n)[:max_steps]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Create spiral coordinates
        theta = np.linspace(0, 4 * np.pi, len(trajectory))
        r = np.linspace(1, 10, len(trajectory))
        
        # Color based on Hamming weight
        hamming_weights = [bin(x).count('1') for x in trajectory]
        
        scatter = ax.scatter(theta, r, c=hamming_weights, cmap='plasma', 
                            s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        # Connect points with lines
        ax.plot(theta, r, 'gray', alpha=0.3, linewidth=0.5)
        
        # Annotate some points
        for i in range(0, len(trajectory), max(1, len(trajectory)//10)):
            ax.annotate(str(trajectory[i]), (theta[i], r[i]), 
                       fontsize=8, ha='center', va='center')
        
        ax.set_title(f'Binary Spiral Evolution of n={n}\n(Color = Hamming Weight)')
        plt.colorbar(scatter, ax=ax, label='Hamming Weight', pad=0.1)
        
        return fig

def demonstrate_visualizations():
    """Create example visualizations"""
    visualizer = BinaryPatternVisualizer()
    
    # Example 1: Binary trajectory heatmap
    print("Creating binary trajectory visualization...")
    fig1 = visualizer.visualize_binary_trajectory(27)
    plt.savefig('binary_trajectory_27.png', dpi=150, bbox_inches='tight')
    print("Saved: binary_trajectory_27.png")
    
    # Example 2: Resonance map
    print("Creating resonance map...")
    fig2 = visualizer.create_resonance_map(1, 1000, sample_size=200)
    plt.savefig('resonance_map_1_1000.png', dpi=150, bbox_inches='tight')
    print("Saved: resonance_map_1_1000.png")
    
    # Example 3: Bit transitions
    print("Creating bit transition visualization...")
    fig3 = visualizer.visualize_bit_transitions(27)
    plt.savefig('bit_transitions_27.png', dpi=150, bbox_inches='tight')
    print("Saved: bit_transitions_27.png")
    
    # Example 4: Binary spiral
    print("Creating binary spiral...")
    fig4 = visualizer.create_binary_spiral(27)
    plt.savefig('binary_spiral_27.png', dpi=150, bbox_inches='tight')
    print("Saved: binary_spiral_27.png")
    
    plt.show()

if __name__ == "__main__":
    demonstrate_visualizations()
