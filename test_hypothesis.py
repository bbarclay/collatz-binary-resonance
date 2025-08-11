#!/usr/bin/env python3
"""
Rigorous testing of the binary-ternary resonance hypothesis.
This code tests whether the shifts s_n = (2^(2n+1) + 1)/3 
have special properties for Collatz sequences.
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from collections import defaultdict

def get_shift(n):
    """Calculate the nth shift value: s_n = (2^(2n+1) + 1)/3"""
    return (2**(2*n + 1) + 1) // 3

def trailing_zeros(num):
    """Count trailing zeros in binary representation"""
    if num == 0:
        return 0
    count = 0
    while num % 2 == 0:
        count += 1
        num //= 2
    return count

def analyze_trailing_zeros_at_shift(shift, sample_size=100000):
    """
    Analyze trailing zero distributions at a given shift value.
    Returns statistics about alignment between n+1 and 3n+1 patterns.
    """
    # Distribution of trailing zeros for n+1
    dist_n_plus_1 = defaultdict(int)
    # Distribution of trailing zeros for 3n+1
    dist_3n_plus_1 = defaultdict(int)
    # Joint distribution
    joint_dist = defaultdict(int)
    
    # Sample odd numbers around the shift
    for offset in range(-sample_size//2, sample_size//2):
        n = shift + 2 * offset  # Keep n odd
        if n > 0:
            tz_n_plus_1 = trailing_zeros(n + 1)
            tz_3n_plus_1 = trailing_zeros(3 * n + 1)
            
            dist_n_plus_1[tz_n_plus_1] += 1
            dist_3n_plus_1[tz_3n_plus_1] += 1
            joint_dist[(tz_n_plus_1, tz_3n_plus_1)] += 1
    
    # Calculate mutual information
    total = sum(joint_dist.values())
    mi = 0
    for (k1, k2), count in joint_dist.items():
        p_joint = count / total
        p_k1 = dist_n_plus_1[k1] / total
        p_k2 = dist_3n_plus_1[k2] / total
        if p_joint > 0:
            mi += p_joint * np.log2(p_joint / (p_k1 * p_k2))
    
    return {
        'mutual_information': mi,
        'dist_n_plus_1': dict(dist_n_plus_1),
        'dist_3n_plus_1': dict(dist_3n_plus_1),
        'joint_dist': dict(joint_dist)
    }

def compare_shift_to_random(n, num_random=100):
    """
    Compare the special shift s_n to random odd values.
    Tests if the shift has statistically significant properties.
    """
    shift = get_shift(n)
    print(f"\nAnalyzing shift s_{n} = {shift} = {bin(shift)}")
    
    # Analyze at the special shift
    shift_results = analyze_trailing_zeros_at_shift(shift)
    shift_mi = shift_results['mutual_information']
    
    # Analyze at random odd values for comparison
    random_mis = []
    for _ in range(num_random):
        # Random odd number in similar range
        random_odd = 2 * np.random.randint(shift//2, shift*2) + 1
        random_results = analyze_trailing_zeros_at_shift(random_odd, sample_size=10000)
        random_mis.append(random_results['mutual_information'])
    
    # Statistical test
    mean_random = np.mean(random_mis)
    std_random = np.std(random_mis)
    z_score = (shift_mi - mean_random) / std_random if std_random > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    
    print(f"Mutual Information at shift: {shift_mi:.6f}")
    print(f"Mean MI at random positions: {mean_random:.6f} ± {std_random:.6f}")
    print(f"Z-score: {z_score:.3f}")
    print(f"P-value: {p_value:.6f}")
    
    if p_value < 0.05:
        print("*** SIGNIFICANT: Shift has special properties! ***")
    else:
        print("Not significant: Shift appears ordinary")
    
    return {
        'shift': shift,
        'shift_mi': shift_mi,
        'random_mean': mean_random,
        'random_std': std_random,
        'z_score': z_score,
        'p_value': p_value
    }

def test_collatz_trajectories_at_shifts(max_n=5):
    """
    Test if numbers near the shifts have special Collatz trajectory properties.
    """
    for n in range(max_n):
        shift = get_shift(n)
        print(f"\nShift s_{n} = {shift}")
        
        # Test trajectory lengths near the shift
        trajectory_lengths = []
        for offset in range(-100, 101):
            test_num = shift + 2 * offset  # Keep odd
            if test_num > 0:
                length = collatz_trajectory_length(test_num)
                trajectory_lengths.append(length)
        
        mean_length = np.mean(trajectory_lengths)
        std_length = np.std(trajectory_lengths)
        
        # Compare to random odd numbers
        random_lengths = []
        for _ in range(1000):
            random_odd = 2 * np.random.randint(1, 2*shift) + 1
            random_lengths.append(collatz_trajectory_length(random_odd))
        
        random_mean = np.mean(random_lengths)
        random_std = np.std(random_lengths)
        
        print(f"  Near shift: mean trajectory = {mean_length:.1f} ± {std_length:.1f}")
        print(f"  Random: mean trajectory = {random_mean:.1f} ± {random_std:.1f}")
        
        # Statistical test
        t_stat, p_value = stats.ttest_ind(trajectory_lengths, random_lengths)
        if p_value < 0.05:
            print(f"  *** Significant difference (p={p_value:.6f}) ***")

def collatz_trajectory_length(n):
    """Calculate the length of Collatz trajectory to reach 1"""
    steps = 0
    while n != 1 and steps < 1000:  # Safety limit
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def verify_mathematical_properties():
    """Verify the claimed mathematical properties of the shift sequence"""
    print("Verifying mathematical properties of shift sequence:\n")
    
    for n in range(8):
        s = get_shift(n)
        
        # Property 1: 3s - 1 = 2^(2n+1)
        prop1 = (3 * s - 1 == 2**(2*n + 1))
        
        # Property 2: Recurrence s_{n+1} = 4s_n - 1
        if n > 0:
            s_prev = get_shift(n-1)
            prop2 = (s == 4 * s_prev - 1)
        else:
            prop2 = True
        
        # Property 3: Binary pattern
        binary = bin(s)[2:]
        expected_ones = set(range(0, 2*n, 2))  # Positions 0, 2, 4, ...
        actual_ones = {i for i, bit in enumerate(reversed(binary)) if bit == '1'}
        prop3 = (expected_ones == actual_ones)
        
        print(f"s_{n} = {s}:")
        print(f"  Binary: {binary}")
        print(f"  3s - 1 = 2^{2*n+1}: {prop1}")
        print(f"  Recurrence holds: {prop2}")
        print(f"  Binary pattern correct: {prop3}")
        print()

def main():
    """Run all tests"""
    print("="*60)
    print("TESTING BINARY-TERNARY RESONANCE HYPOTHESIS")
    print("="*60)
    
    # First verify the mathematical properties
    verify_mathematical_properties()
    
    print("="*60)
    print("TESTING TRAILING ZERO ALIGNMENT")
    print("="*60)
    
    # Test the alignment hypothesis for small shifts
    results = []
    for n in range(5):
        result = compare_shift_to_random(n, num_random=50)
        results.append(result)
    
    print("\n" + "="*60)
    print("TESTING COLLATZ TRAJECTORY PROPERTIES")
    print("="*60)
    
    test_collatz_trajectories_at_shifts(max_n=5)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    significant_shifts = [r for r in results if r['p_value'] < 0.05]
    if significant_shifts:
        print(f"\nFound {len(significant_shifts)} shifts with significant properties:")
        for r in significant_shifts:
            print(f"  s_{results.index(r)} = {r['shift']} (p={r['p_value']:.6f})")
    else:
        print("\nNo shifts showed statistically significant special properties.")
    
    print("\nThis analysis provides rigorous testing of the hypothesis.")
    print("Further investigation would require larger samples and additional metrics.")

if __name__ == "__main__":
    main()
