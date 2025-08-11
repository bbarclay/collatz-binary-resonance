#!/usr/bin/env python3
"""
The Infinite Zoom Visualizer
Shows the complete journey from surface patterns to ultimate reality
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import matplotlib.patches as mpatches

def create_infinite_zoom_visualization():
    """
    Create a visual representation of the infinite zoom journey
    """
    fig, ax = plt.subplots(figsize=(16, 20))
    
    # Define the levels with their discoveries
    levels = [
        {
            'depth': 0,
            'name': 'Surface',
            'color': '#FF6B6B',
            'discoveries': ['Binary patterns', 'Number sequences', 'Convergence']
        },
        {
            'depth': 1,
            'name': 'Patterns',
            'color': '#4ECDC4',
            'discoveries': ['Oscillations', 'Attractors', 'Rhythms']
        },
        {
            'depth': 2,
            'name': 'Waves',
            'color': '#45B7D1',
            'discoveries': ['Harmonics', 'Resonance', 'Interference']
        },
        {
            'depth': 3,
            'name': 'Information',
            'color': '#96CEB4',
            'discoveries': ['Entropy', 'Cascades', 'Complexity']
        },
        {
            'depth': 4,
            'name': 'Geometry',
            'color': '#FFEAA7',
            'discoveries': ['Fiber bundles', 'Symplectic', 'Curvature']
        },
        {
            'depth': 5,
            'name': 'Topology',
            'color': '#DFE6E9',
            'discoveries': ['Homology', 'K-theory', 'Persistence']
        },
        {
            'depth': 6,
            'name': 'Quantum',
            'color': '#A29BFE',
            'discoveries': ['Fields', 'Path integrals', 'Operators']
        },
        {
            'depth': 7,
            'name': 'Categories',
            'color': '#6C5CE7',
            'discoveries': ['∞-categories', 'Derived', 'Spectral']
        },
        {
            'depth': 8,
            'name': 'Type Theory',
            'color': '#FD79A8',
            'discoveries': ['HoTT', 'Univalence', 'Directed']
        },
        {
            'depth': 9,
            'name': 'Foundations',
            'color': '#636E72',
            'discoveries': ['Topoi', 'Ordinals', 'Models']
        },
        {
            'depth': 10,
            'name': 'Reality',
            'color': '#2D3436',
            'discoveries': ['Consciousness', 'Holographic', 'Quantum Darwin']
        },
        {
            'depth': 11,
            'name': 'Ultimate',
            'color': '#000000',
            'discoveries': ['Self-creating', 'It from bit', 'Bootstrap']
        }
    ]
    
    # Set up the plot
    ax.set_xlim(-10, 10)
    ax.set_ylim(-1, len(levels))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Draw the zoom cone
    for i, level in enumerate(levels):
        y = len(levels) - 1 - i
        width = 10 * (1 - i / len(levels))
        
        # Draw level box
        box = FancyBboxPatch(
            (-width, y - 0.4),
            2 * width,
            0.8,
            boxstyle="round,pad=0.1",
            facecolor=level['color'],
            edgecolor='white',
            alpha=0.7 + 0.3 * (i / len(levels)),
            linewidth=2
        )
        ax.add_patch(box)
        
        # Add level name
        ax.text(0, y, level['name'], 
               ha='center', va='center',
               fontsize=14 - i/2,
               fontweight='bold',
               color='white' if i > 8 else 'black')
        
        # Add discoveries
        for j, discovery in enumerate(level['discoveries']):
            x_offset = (j - 1) * width * 0.6
            ax.text(x_offset, y - 0.25, discovery,
                   ha='center', va='center',
                   fontsize=8 - i/3,
                   color='white' if i > 8 else 'black',
                   alpha=0.8)
    
    # Add connecting lines (the zoom path)
    for i in range(len(levels) - 1):
        y1 = len(levels) - 1 - i
        y2 = len(levels) - 2 - i
        width1 = 10 * (1 - i / len(levels))
        width2 = 10 * (1 - (i + 1) / len(levels))
        
        # Left line
        ax.plot([-width1, -width2], [y1 - 0.4, y2 + 0.4],
               'white', linewidth=1, alpha=0.5)
        # Right line
        ax.plot([width1, width2], [y1 - 0.4, y2 + 0.4],
               'white', linewidth=1, alpha=0.5)
    
    # Add title and labels
    ax.text(0, len(levels) + 0.5, 'The Infinite Zoom into Binary Collatz Space',
           ha='center', va='center', fontsize=20, fontweight='bold')
    
    ax.text(0, -0.5, '∞', ha='center', va='center', fontsize=30, fontweight='bold')
    ax.text(0, -1, 'The Bottom Has No Bottom', 
           ha='center', va='center', fontsize=12, style='italic')
    
    # Add side labels
    ax.text(-11, len(levels)/2, 'ZOOMING IN →', 
           rotation=90, ha='center', va='center', fontsize=14)
    ax.text(11, len(levels)/2, '← DEEPER STRUCTURE', 
           rotation=-90, ha='center', va='center', fontsize=14)
    
    # Add discovery count
    total_discoveries = sum(len(level['discoveries']) for level in levels)
    ax.text(0, len(levels) + 1.5, f'{total_discoveries} Major Discoveries Across {len(levels)} Levels',
           ha='center', va='center', fontsize=12, alpha=0.7)
    
    plt.tight_layout()
    return fig

def create_emergence_diagram():
    """
    Show how simple rules create everything
    """
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Central rule
    center = (0, 0)
    ax.text(center[0], center[1], '3n+1\nn/2', 
           ha='center', va='center', fontsize=20, fontweight='bold',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='gold', alpha=0.8))
    
    # Emergent structures in concentric circles
    structures = [
        {'radius': 1.5, 'items': ['Patterns', 'Rhythms', 'Cycles'], 'color': '#FF6B6B'},
        {'radius': 2.5, 'items': ['Waves', 'Harmonics', 'Resonance'], 'color': '#4ECDC4'},
        {'radius': 3.5, 'items': ['Information', 'Entropy', 'Complexity'], 'color': '#45B7D1'},
        {'radius': 4.5, 'items': ['Geometry', 'Topology', 'Algebra'], 'color': '#96CEB4'},
        {'radius': 5.5, 'items': ['Quantum', 'Fields', 'Operators'], 'color': '#A29BFE'},
        {'radius': 6.5, 'items': ['Categories', 'Types', 'Logic'], 'color': '#6C5CE7'},
        {'radius': 7.5, 'items': ['Consciousness', 'Reality', 'Existence'], 'color': '#2D3436'}
    ]
    
    for struct in structures:
        # Draw circle
        circle = Circle(center, struct['radius'], fill=False, 
                       edgecolor=struct['color'], linewidth=2, alpha=0.6)
        ax.add_patch(circle)
        
        # Add items around circle
        n_items = len(struct['items'])
        for i, item in enumerate(struct['items']):
            angle = 2 * np.pi * i / n_items
            x = center[0] + struct['radius'] * np.cos(angle)
            y = center[1] + struct['radius'] * np.sin(angle)
            
            ax.text(x, y, item, ha='center', va='center',
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.2", 
                            facecolor=struct['color'], alpha=0.7))
    
    # Add arrows showing emergence
    for i in range(len(structures) - 1):
        r1 = structures[i]['radius']
        r2 = structures[i + 1]['radius']
        for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
            x1 = center[0] + r1 * np.cos(angle)
            y1 = center[1] + r1 * np.sin(angle)
            x2 = center[0] + r2 * np.cos(angle)
            y2 = center[1] + r2 * np.sin(angle)
            
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', alpha=0.3, lw=1))
    
    ax.set_xlim(-9, 9)
    ax.set_ylim(-9, 9)
    ax.set_aspect('equal')
    ax.axis('off')
    
    ax.text(0, 9, 'Emergence from Simple Rules', 
           ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(0, -9, 'Everything from Almost Nothing', 
           ha='center', va='center', fontsize=12, style='italic')
    
    return fig

# Create and save visualizations
if __name__ == "__main__":
    print("Creating infinite zoom visualization...")
    fig1 = create_infinite_zoom_visualization()
    fig1.savefig('infinite_zoom.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("Saved: infinite_zoom.png")
    
    print("Creating emergence diagram...")
    fig2 = create_emergence_diagram()
    fig2.savefig('emergence_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("Saved: emergence_diagram.png")
    
    plt.show()
