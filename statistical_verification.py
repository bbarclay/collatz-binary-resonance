#!/usr/bin/env python3
"""
Specific verification of statistical claims about p-values and variance ratios.
"""

import numpy as np
from scipy import stats
import random

def collatz_trajectory_length(n):
    """Compute Collatz trajectory length"""
    steps = 0
    while n != 1 and steps < 10000:  # Safety limit
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3*n + 1
        steps += 1
    return steps if n == 1 else -1  # Return -1 if didn't reach 1

def verify_statistical_claims():
    """Verify the statistical claims with smaller samples for verification"""
    print("=== VERIFYING STATISTICAL CLAIMS ===")
    
    # The sequence values
    sequence_values = [
        (2, 11),
        (3, 43),
        (4, 171),
        (5, 683)
    ]
    
    sample_size = 1000  # Smaller for verification
    
    for n, s_n in sequence_values:
        print(f"\nAnalyzing shift s_{n} = {s_n}:")
        
        # Sample around the shift
        shift_trajectories = []
        for offset in range(-sample_size//2, sample_size//2):
            test_val = s_n + 2*offset  # Keep odd
            if test_val > 0:
                traj_len = collatz_trajectory_length(test_val)
                if traj_len > 0:  # Valid trajectory
                    shift_trajectories.append(traj_len)
        
        # Random control group of similar magnitude
        control_trajectories = []
        random.seed(42)  # Reproducible
        for _ in range(sample_size):
            # Generate random odd number in similar range
            rand_val = 2*random.randint(s_n//2, 2*s_n) + 1
            traj_len = collatz_trajectory_length(rand_val)
            if traj_len > 0:
                control_trajectories.append(traj_len)
        
        if len(shift_trajectories) > 100 and len(control_trajectories) > 100:
            # Statistical comparison
            t_stat, p_value = stats.ttest_ind(shift_trajectories, control_trajectories)
            
            # Variance ratio
            shift_var = np.var(shift_trajectories)
            control_var = np.var(control_trajectories)
            var_ratio = shift_var / control_var if control_var > 0 else float('inf')
            
            # F-test for variance equality
            f_stat = var_ratio if var_ratio >= 1 else 1/var_ratio
            df1 = len(shift_trajectories) - 1
            df2 = len(control_trajectories) - 1
            var_p_value = 2 * (1 - stats.f.cdf(f_stat, df1, df2))  # Two-tailed
            
            print(f"  Mean trajectory lengths: {np.mean(shift_trajectories):.2f} vs {np.mean(control_trajectories):.2f}")
            print(f"  t-test p-value: {p_value:.6f}")
            print(f"  Variance ratio: {var_ratio:.3f}")
            print(f"  Variance test p-value: {var_p_value:.6f}")
            
            # Check claims
            if p_value < 0.0001:
                print(f"  ✓ p-value < 10^-4: {p_value:.6f} < 0.0001")
            else:
                print(f"  ❌ p-value NOT < 10^-4: {p_value:.6f} >= 0.0001")
            
            if var_p_value < 0.05:
                print(f"  ✓ Significant variance difference: p = {var_p_value:.6f}")
            else:
                print(f"  ❌ No significant variance difference: p = {var_p_value:.6f}")
        else:
            print(f"  ❌ Insufficient valid trajectories for analysis")

def verify_2adic_convergence():
    """Verify 2-adic convergence claim"""
    print("\n=== VERIFYING 2-ADIC CONVERGENCE ===")
    
    def binary_inverse_sequence(n):
        return (2**(2*n + 1) + 1) // 3
    
    def two_adic_distance(a, b):
        """Compute 2-adic distance |a - b|_2"""
        if a == b:
            return 0
        diff = abs(a - b)
        # Count trailing zeros
        trailing_zeros = 0
        while diff % 2 == 0:
            diff //= 2
            trailing_zeros += 1
        return 2**(-trailing_zeros)
    
    print("2-adic distances between consecutive terms:")
    for n in range(1, 8):
        s_n = binary_inverse_sequence(n)
        s_n_minus_1 = binary_inverse_sequence(n-1)
        
        distance = two_adic_distance(s_n, s_n_minus_1)
        theoretical = 2**(-2*n+1)
        
        print(f"  |s_{n} - s_{n-1}|_2 = {distance:.6f}, theoretical = {theoretical:.6f}")
        
        if abs(distance - theoretical) < 1e-10:
            print(f"    ✓ Match!")
        else:
            print(f"    ❌ Mismatch!")

def main():
    print("STATISTICAL AND 2-ADIC VERIFICATION")
    print("="*50)
    
    verify_statistical_claims()
    verify_2adic_convergence()
    
    print("\n" + "="*50)
    print("Note: Statistical results may vary due to randomness,")
    print("but the mathematical patterns should be consistent.")
    print("="*50)

if __name__ == "__main__":
    main()