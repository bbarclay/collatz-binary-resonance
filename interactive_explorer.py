#!/usr/bin/env python3
"""
Interactive Binary Resonance Explorer
Run this to explore the discoveries yourself!
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
import os

class InteractiveExplorer:
    def __init__(self):
        self.current_n = 27
        self.trajectory_cache = {}
        
    def collatz_step(self, n):
        return 3 * n + 1 if n & 1 else n >> 1
    
    def get_trajectory(self, n, max_steps=500):
        if n in self.trajectory_cache:
            return self.trajectory_cache[n]
            
        trajectory = [n]
        current = n
        while current != 1 and len(trajectory) < max_steps:
            current = self.collatz_step(current)
            trajectory.append(current)
        
        self.trajectory_cache[n] = trajectory
        return trajectory
    
    def explore_number(self, n):
        """Interactive exploration of a single number"""
        print(f"\n{'='*70}")
        print(f"EXPLORING n = {n} (binary: {bin(n)[2:]})")
        print(f"{'='*70}")
        
        trajectory = self.get_trajectory(n)
        
        # Basic stats
        print(f"\n📊 BASIC STATISTICS:")
        print(f"  Trajectory length: {len(trajectory)} steps")
        print(f"  Maximum value: {max(trajectory)} ({bin(max(trajectory))[2:]})")
        print(f"  Maximum binary width: {max(len(bin(x)[2:]) for x in trajectory)} bits")
        
        # Binary evolution (first 20 steps)
        print(f"\n🔄 BINARY EVOLUTION (first 20 steps):")
        print("  Step | Value      | Binary           | Operation | Width | Density")
        print("  -----|------------|------------------|-----------|-------|--------")
        
        for i in range(min(20, len(trajectory))):
            num = trajectory[i]
            binary = bin(num)[2:]
            width = len(binary)
            density = binary.count('1') / width
            
            if i < len(trajectory) - 1:
                op = "3n+1" if num & 1 else "n/2 "
            else:
                op = "END "
            
            print(f"  {i:4d} | {num:10d} | {binary:16s} | {op:9s} | {width:5d} | {density:.3f}")
        
        # Find patterns
        print(f"\n🎯 PATTERN DISCOVERIES:")
        
        # Palindromes
        palindromes = []
        for i, num in enumerate(trajectory):
            binary = bin(num)[2:]
            if binary == binary[::-1] and len(binary) > 1:
                palindromes.append((i, num, binary))
        
        if palindromes:
            print(f"  Binary palindromes found: {len(palindromes)}")
            for step, val, binary in palindromes[:3]:
                print(f"    Step {step}: {binary} ({val})")
        
        # Powers of 2
        powers_of_2 = []
        for i, num in enumerate(trajectory):
            if (num & (num - 1)) == 0 and num > 1:
                powers_of_2.append((i, num, int(np.log2(num))))
        
        if powers_of_2:
            print(f"  Powers of 2 encountered: {len(powers_of_2)}")
            for step, val, power in powers_of_2[:3]:
                print(f"    Step {step}: 2^{power} = {val}")
        
        # Operation rhythm
        ops = ''.join('O' if trajectory[i] & 1 else 'E' for i in range(min(100, len(trajectory)-1)))
        print(f"  Operation rhythm: {ops[:50]}...")
        
        # Information cascade
        print(f"\n📈 INFORMATION CASCADE:")
        info_values = []
        for num in trajectory[:50]:
            binary = bin(num)[2:]
            ones = binary.count('1')
            if 0 < ones < len(binary):
                p1 = ones / len(binary)
                p0 = 1 - p1
                entropy = -(p1 * np.log2(p1) + p0 * np.log2(p0))
                info = len(binary) * entropy
            else:
                info = 0
            info_values.append(info)
        
        if info_values:
            max_info = max(info_values)
            max_info_step = info_values.index(max_info)
            print(f"  Peak information: {max_info:.2f} bits at step {max_info_step}")
            print(f"  Information visualization (first 30 steps):")
            for i in range(min(30, len(info_values))):
                bar = '█' * int(info_values[i])
                print(f"    {i:3d}: {bar}")
        
        # Binary center of mass
        print(f"\n🌊 BINARY CENTER OF MASS WAVE:")
        com_values = []
        for num in trajectory[:30]:
            binary = bin(num)[2:]
            positions = [i for i, bit in enumerate(reversed(binary)) if bit == '1']
            com = sum(positions) / len(positions) if positions else 0
            com_values.append(com)
        
        print("  First 30 steps:")
        for i, com in enumerate(com_values):
            visual = '.' * int(com) + '●'
            print(f"    {i:3d}: {visual} ({com:.1f})")
        
        return trajectory
    
    def compare_numbers(self, n1, n2):
        """Compare two numbers for resonance"""
        print(f"\n{'='*70}")
        print(f"COMPARING n={n1} and n={n2}")
        print(f"{'='*70}")
        
        traj1 = self.get_trajectory(n1, 200)
        traj2 = self.get_trajectory(n2, 200)
        
        # Compare basic properties
        print(f"\n📊 COMPARISON:")
        print(f"  {'Property':<20} | n={n1:<6} | n={n2:<6}")
        print(f"  {'-'*20}-+-{'-'*8}-+-{'-'*8}")
        print(f"  {'Binary':<20} | {bin(n1)[2:]:<8} | {bin(n2)[2:]:<8}")
        print(f"  {'Trajectory length':<20} | {len(traj1):<8} | {len(traj2):<8}")
        print(f"  {'Maximum value':<20} | {max(traj1):<8} | {max(traj2):<8}")
        print(f"  {'Max binary width':<20} | {max(len(bin(x)[2:]) for x in traj1):<8} | {max(len(bin(x)[2:]) for x in traj2):<8}")
        
        # Find common values
        common = set(traj1) & set(traj2)
        print(f"\n  Common values visited: {len(common)}")
        if common:
            common_list = sorted(common)[:10]
            print(f"    First few: {common_list}")
        
        # Compare operation rhythms
        ops1 = ''.join('O' if traj1[i] & 1 else 'E' for i in range(min(50, len(traj1)-1)))
        ops2 = ''.join('O' if traj2[i] & 1 else 'E' for i in range(min(50, len(traj2)-1)))
        
        # Find matching segments
        matches = 0
        for i in range(min(len(ops1), len(ops2))):
            if ops1[i] == ops2[i]:
                matches += 1
        
        similarity = matches / min(len(ops1), len(ops2)) * 100
        print(f"\n  Rhythm similarity: {similarity:.1f}%")
        print(f"    n={n1}: {ops1[:30]}...")
        print(f"    n={n2}: {ops2[:30]}...")
    
    def visualize_discoveries(self, n):
        """Create visualizations of the discoveries"""
        trajectory = self.get_trajectory(n, 200)
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(f'Binary Resonance Discoveries for n={n}', fontsize=16)
        
        # 1. Binary width evolution
        widths = [len(bin(x)[2:]) for x in trajectory]
        axes[0, 0].plot(widths[:100], 'b-', linewidth=2)
        axes[0, 0].fill_between(range(len(widths[:100])), widths[:100], alpha=0.3)
        axes[0, 0].set_title('Binary Width Evolution')
        axes[0, 0].set_xlabel('Step')
        axes[0, 0].set_ylabel('Bits')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Hamming weight
        hamming = [bin(x).count('1') for x in trajectory]
        axes[0, 1].bar(range(len(hamming[:100])), hamming[:100], color='purple', alpha=0.6)
        axes[0, 1].set_title('Hamming Weight (# of 1s)')
        axes[0, 1].set_xlabel('Step')
        axes[0, 1].set_ylabel('Count')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Bit density
        densities = [hamming[i]/widths[i] if widths[i] > 0 else 0 for i in range(len(hamming))]
        axes[0, 2].plot(densities[:100], 'g-', linewidth=2)
        axes[0, 2].axhline(y=0.5, color='r', linestyle='--', alpha=0.5)
        axes[0, 2].set_title('Bit Density Evolution')
        axes[0, 2].set_xlabel('Step')
        axes[0, 2].set_ylabel('Density (0-1)')
        axes[0, 2].grid(True, alpha=0.3)
        
        # 4. Information content
        info = []
        for num in trajectory[:100]:
            binary = bin(num)[2:]
            ones = binary.count('1')
            if 0 < ones < len(binary):
                p1 = ones / len(binary)
                p0 = 1 - p1
                entropy = -(p1 * np.log2(p1) + p0 * np.log2(p0))
                info.append(len(binary) * entropy)
            else:
                info.append(0)
        
        axes[1, 0].plot(info, 'orange', linewidth=2)
        axes[1, 0].fill_between(range(len(info)), info, alpha=0.3, color='orange')
        axes[1, 0].set_title('Information Content')
        axes[1, 0].set_xlabel('Step')
        axes[1, 0].set_ylabel('Bits')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 5. Value evolution (log scale)
        axes[1, 1].semilogy(trajectory[:100], 'r-', linewidth=2)
        axes[1, 1].set_title('Value Evolution (log scale)')
        axes[1, 1].set_xlabel('Step')
        axes[1, 1].set_ylabel('Value')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 6. Binary heatmap
        binary_matrix = np.zeros((min(50, len(trajectory)), 20))
        for i in range(min(50, len(trajectory))):
            binary = bin(trajectory[i])[2:].zfill(20)[-20:]
            for j, bit in enumerate(binary):
                binary_matrix[i, j] = int(bit)
        
        im = axes[1, 2].imshow(binary_matrix, cmap='YlOrRd', aspect='auto')
        axes[1, 2].set_title('Binary Pattern Heatmap')
        axes[1, 2].set_xlabel('Bit Position')
        axes[1, 2].set_ylabel('Step')
        plt.colorbar(im, ax=axes[1, 2])
        
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def interactive_menu(self):
        """Interactive menu for exploration"""
        while True:
            print(f"\n{'='*70}")
            print("BINARY RESONANCE EXPLORER - Interactive Menu")
            print(f"{'='*70}")
            print("\n1. Explore a specific number")
            print("2. Compare two numbers")
            print("3. Find patterns in a range")
            print("4. Visualize discoveries")
            print("5. Test famous numbers")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                try:
                    n = int(input("Enter a number to explore: "))
                    if n > 0:
                        self.explore_number(n)
                    else:
                        print("Please enter a positive integer.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            elif choice == '2':
                try:
                    n1 = int(input("Enter first number: "))
                    n2 = int(input("Enter second number: "))
                    if n1 > 0 and n2 > 0:
                        self.compare_numbers(n1, n2)
                    else:
                        print("Please enter positive integers.")
                except ValueError:
                    print("Invalid input. Please enter numbers.")
            
            elif choice == '3':
                try:
                    start = int(input("Enter start of range: "))
                    end = int(input("Enter end of range: "))
                    if start > 0 and end > start:
                        self.find_patterns_in_range(start, end)
                    else:
                        print("Please enter valid range.")
                except ValueError:
                    print("Invalid input.")
            
            elif choice == '4':
                try:
                    n = int(input("Enter a number to visualize: "))
                    if n > 0:
                        self.visualize_discoveries(n)
                    else:
                        print("Please enter a positive integer.")
                except ValueError:
                    print("Invalid input.")
            
            elif choice == '5':
                print("\n🌟 FAMOUS NUMBERS IN COLLATZ:")
                famous = {
                    27: "Takes 111 steps, reaches 9232",
                    31: "All ones in binary (11111)",
                    837799: "Longest trajectory under 1 million",
                    63728127: "Longest under 100 million",
                    7: "Simple but interesting (111 in binary)",
                    15: "Four ones (1111)",
                    255: "Eight ones (11111111)"
                }
                
                for num, description in famous.items():
                    print(f"  {num}: {description}")
                
                n = int(input("\nWhich one to explore? "))
                if n in famous:
                    self.explore_number(n)
            
            elif choice == '6':
                print("\nThank you for exploring the Binary Resonance!")
                print("The patterns continue infinitely... 🌊")
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    def find_patterns_in_range(self, start, end):
        """Find interesting patterns in a range"""
        print(f"\n🔍 SEARCHING FOR PATTERNS IN [{start}, {end}]...")
        
        patterns = {
            'palindromes': [],
            'all_ones': [],
            'fast_convergence': [],
            'slow_convergence': []
        }
        
        for n in range(start, end + 1):
            trajectory = self.get_trajectory(n)
            
            # Check for palindromes
            for num in trajectory:
                binary = bin(num)[2:]
                if binary == binary[::-1] and len(binary) > 2:
                    patterns['palindromes'].append(n)
                    break
            
            # Check for all ones
            binary = bin(n)[2:]
            if all(bit == '1' for bit in binary):
                patterns['all_ones'].append(n)
            
            # Check convergence speed
            if len(trajectory) < 20:
                patterns['fast_convergence'].append(n)
            elif len(trajectory) > 100:
                patterns['slow_convergence'].append(n)
        
        print(f"\n📊 PATTERNS FOUND:")
        print(f"  Numbers creating palindromes: {len(patterns['palindromes'])}")
        if patterns['palindromes']:
            print(f"    Examples: {patterns['palindromes'][:5]}")
        
        print(f"  All-ones numbers: {patterns['all_ones']}")
        print(f"  Fast convergence (<20 steps): {len(patterns['fast_convergence'])}")
        print(f"  Slow convergence (>100 steps): {len(patterns['slow_convergence'])}")
        if patterns['slow_convergence']:
            print(f"    Examples: {patterns['slow_convergence'][:5]}")

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║               BINARY RESONANCE EXPLORER                         ║
║                                                                  ║
║     Discover the Hidden Patterns in Collatz Sequences           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

Welcome to the interactive explorer for binary patterns in the
Collatz conjecture! This tool lets you explore the fascinating
discoveries we've made by zooming into the binary structure.

Ready to see what happens when we keep zooming in? Let's go!
    """)
    
    explorer = InteractiveExplorer()
    
    # Start with a demonstration
    print("\n🎯 Let's start with a demonstration using n=27...")
    input("Press Enter to continue...")
    explorer.explore_number(27)
    
    # Then go to interactive menu
    explorer.interactive_menu()

if __name__ == "__main__":
    main()
