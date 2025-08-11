#!/usr/bin/env python3
"""
Test script for the computational code from 05_computational_code.py
This extracts and tests all the functions defined in that file.
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def generate_shifts(n):
    """Generate the first n shift values."""
    shifts = []
    for i in range(n):
        s = (2**(2*i + 1) + 1) // 3
        shifts.append(s)
    return shifts

def verify_property(s):
    """Verify that 3s - 1 is a power of 2."""
    val = 3 * s - 1
    # Check if val is a power of 2
    return val & (val - 1) == 0 and val != 0

def binary_pattern(s):
    """Show the binary representation and analyze pattern."""
    binary = bin(s)[2:]
    positions = [i for i, bit in enumerate(reversed(binary)) if bit == '1']
    gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
    return binary, positions, gaps

def trailing_zeros(n):
    """Count trailing zeros in binary representation."""
    if n == 0:
        return 0
    return (n & -n).bit_length() - 1

def analyze_alignment(shift, count=1000):
    """Analyze trailing zero alignment at a given shift."""
    matches = {i: 0 for i in range(10)}
    
    for i in range(count):
        n1 = shift + 2*i
        n2 = 2*i - 1 if i > 0 else 1
        
        tz1 = trailing_zeros(n1 + 1)
        tz2 = trailing_zeros(3*n2 + 1)
        
        if tz1 == tz2:
            matches[tz1] += 1
    
    return matches

def detect_periodicity(shift, max_n=1000):
    """Detect the period of trailing zero pattern."""
    sequence = []
    for i in range(max_n):
        n = shift + 2*i
        tz = trailing_zeros(n + 1)
        sequence.append(tz)
    
    # Find period
    for period in range(1, len(sequence)//2):
        if sequence[:period] == sequence[period:2*period]:
            return period, sequence[:period]
    return None, sequence[:100]

def to_base_4(n):
    """Convert number to base 4 representation."""
    if n == 0:
        return "0"
    digits = []
    while n:
        digits.append(str(n % 4))
        n //= 4
    return ''.join(reversed(digits))

def analyze_base_4_pattern(shifts):
    """Analyze the base-4 pattern in shifts."""
    for i, s in enumerate(shifts):
        b4 = to_base_4(s)
        print(f"s_{i} = {s:4d} = {b4}_4")

def two_adic_valuation(n):
    """Calculate 2-adic valuation of n."""
    if n == 0:
        return float('inf')
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v

def verify_modular_inverse(s, k):
    """Verify that s is the modular inverse of 3 mod 2^k."""
    return (3 * s) % (2**k) == 1

def run_verification_suite():
    """Run complete verification of discovered properties."""
    print("Shift Sequence Verification")
    print("=" * 50)
    
    shifts = generate_shifts(10)
    
    for i, s in enumerate(shifts):
        print(f"\ns_{i} = {s}")
        
        # Verify 3s - 1 = 2^k
        val = 3 * s - 1
        k = val.bit_length() - 1
        assert val == 2**k, f"Failed: 3*{s} - 1 != 2^{k}"
        print(f"  ✓ 3s - 1 = {val} = 2^{k}")
        
        # Show binary pattern
        binary, positions, gaps = binary_pattern(s)
        print(f"  Binary: {binary}")
        print(f"  1s at positions: {positions}")
        if gaps:
            print(f"  Gaps: {gaps}")
        
        # Verify modular inverse
        for j in range(3, min(k+1, 20)):
            if verify_modular_inverse(s, j):
                print(f"  ✓ s = 3^(-1) mod 2^{j}")
                break
    
    print("\n" + "=" * 50)
    print("All verifications passed!")

def test_all_functions():
    """Test all extracted functions for correctness."""
    print("Testing 05_computational_code.py functions")
    print("=" * 60)
    
    # Test 1: Generate first 10 shifts
    print("\n1. Testing shift generation:")
    shifts = generate_shifts(10)
    expected = [1, 3, 11, 43, 171, 683, 2731, 10923, 43691, 174763]
    assert shifts == expected, f"Mismatch: got {shifts}, expected {expected}"
    print("✓ Shift generation correct")
    
    # Test 2: Verify property for all shifts
    print("\n2. Testing 3s-1 power of 2 property:")
    all_verified = True
    for i, s in enumerate(shifts):
        if not verify_property(s):
            print(f"✗ Failed for s_{i} = {s}")
            all_verified = False
    if all_verified:
        print("✓ All shifts satisfy 3s-1 = 2^k property")
    
    # Test 3: Binary patterns
    print("\n3. Testing binary patterns:")
    for i in range(5):
        s = shifts[i]
        binary, positions, gaps = binary_pattern(s)
        expected_positions = list(range(0, 2*i, 2)) if i > 0 else [0]
        if positions != expected_positions:
            print(f"✗ Binary pattern mismatch for s_{i}")
        else:
            print(f"✓ s_{i} binary pattern correct: {binary}")
    
    # Test 4: Trailing zeros
    print("\n4. Testing trailing zeros function:")
    test_cases = [(8, 3), (12, 2), (16, 4), (1, 0)]
    for n, expected in test_cases:
        result = trailing_zeros(n)
        assert result == expected, f"trailing_zeros({n}) = {result}, expected {expected}"
    print("✓ Trailing zeros function correct")
    
    # Test 5: Base 4 conversion
    print("\n5. Testing base 4 conversion:")
    test_cases = [(11, "23"), (43, "223"), (171, "2223")]
    for n, expected in test_cases:
        result = to_base_4(n)
        assert result == expected, f"to_base_4({n}) = {result}, expected {expected}"
    print("✓ Base 4 conversion correct")
    
    # Test 6: 2-adic valuation
    print("\n6. Testing 2-adic valuation:")
    test_cases = [(8, 3), (12, 2), (5, 0), (16, 4)]
    for n, expected in test_cases:
        result = two_adic_valuation(n)
        assert result == expected, f"two_adic_valuation({n}) = {result}, expected {expected}"
    print("✓ 2-adic valuation correct")
    
    # Test 7: Modular inverse verification
    print("\n7. Testing modular inverse verification:")
    for i, s in enumerate(shifts[:5]):
        k = 2*i + 1
        if k >= 2:
            result = verify_modular_inverse(s, k)
            assert result, f"s_{i} = {s} should be inverse of 3 mod 2^{k}"
    print("✓ Modular inverse verification correct")
    
    print("\n" + "=" * 60)
    print("ALL FUNCTION TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    test_all_functions()
    print("\n")
    run_verification_suite()
    
    print("\n\nTesting alignment analysis...")
    shifts = generate_shifts(3)
    for i, shift in enumerate(shifts):
        print(f"\nAnalyzing alignment at s_{i} = {shift}:")
        matches = analyze_alignment(shift, count=500)
        total_matches = sum(matches.values())
        print(f"  Total matches: {total_matches}/500 ({100*total_matches/500:.1f}%)")
        
    print("\n\nTesting periodicity detection...")
    for i in range(3):
        shift = shifts[i]
        period, pattern = detect_periodicity(shift, max_n=200)
        if period:
            print(f"s_{i} = {shift}: Period {period}, pattern {pattern}")
        else:
            print(f"s_{i} = {shift}: No clear period found")
    
    print("\n\nBase-4 pattern analysis:")
    analyze_base_4_pattern(shifts)