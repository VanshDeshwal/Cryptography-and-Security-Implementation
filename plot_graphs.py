import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def create_plots():
    """
    Create comprehensive plots for sorting algorithm analysis including normalization
    """
    # Check if the results file exists
    if not os.path.exists('detailed_results.csv'):
        print("Error: detailed_results.csv not found!")
        print("Please make sure the detailed_results.csv file is in the current directory.")
        return
    
    # Read the data
    df = pd.read_csv('detailed_results.csv')
    
    # Set up the plotting style
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (12, 8)
    
    # Get unique algorithms and sizes
    algorithms = df['Algorithm'].unique()
    sizes = sorted(df['Size'].unique())
    
    print(f"Found data for algorithms: {', '.join(algorithms)}")
    print(f"Array sizes: {sizes}")
    
    # Create color palette
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    color_map = {algo: colors[i] for i, algo in enumerate(algorithms)}
    
    print("\nGenerating comprehensive graphs...")

    # Figure 1: Average Comparisons vs Array Size
    plt.figure(figsize=(12, 8))
    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        plt.plot(algo_data['Size'], algo_data['Avg_Comparisons'], 
                marker='o', linewidth=3, markersize=8, label=algo, color=color_map[algo])
    
    plt.xlabel('Array Size', fontsize=14)
    plt.ylabel('Average Number of Comparisons', fontsize=14)
    plt.title('Sorting Algorithm Performance: Average Comparisons', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Log scale for better visibility
    plt.tight_layout()
    plt.savefig('comparisons_vs_size.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: comparisons_vs_size.png")
    plt.show()

    # Figure 2: Average Swaps vs Array Size
    plt.figure(figsize=(12, 8))
    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        plt.plot(algo_data['Size'], algo_data['Avg_Swaps'], 
                marker='s', linewidth=3, markersize=8, label=algo, color=color_map[algo])
    
    plt.xlabel('Array Size', fontsize=14)
    plt.ylabel('Average Number of Swaps', fontsize=14)
    plt.title('Sorting Algorithm Performance: Average Swaps', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Log scale for better visibility
    plt.tight_layout()
    plt.savefig('swaps_vs_size.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: swaps_vs_size.png")
    plt.show()

    # Figure 3: Combined Analysis for Array Size 1000
    size_1000 = df[df['Size'] == 1000]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Comparisons for size 1000
    algorithms_list = size_1000['Algorithm'].tolist()
    avg_comp = size_1000['Avg_Comparisons'].tolist()
    min_comp = size_1000['Min_Comparisons'].tolist()
    max_comp = size_1000['Max_Comparisons'].tolist()

    x_pos = np.arange(len(algorithms_list))
    bars1 = ax1.bar(x_pos, avg_comp, alpha=0.8, 
                    color=[color_map[algo] for algo in algorithms_list])

    # Add error bars showing min-max range
    yerr = [np.array(avg_comp) - np.array(min_comp), 
            np.array(max_comp) - np.array(avg_comp)]
    ax1.errorbar(x_pos, avg_comp, yerr=yerr, fmt='none', capsize=5, capthick=2, color='black')

    ax1.set_xlabel('Sorting Algorithm', fontsize=12)
    ax1.set_ylabel('Number of Comparisons', fontsize=12)
    ax1.set_title('Comparisons for Array Size 1000\n(with Min-Max Range)', fontsize=14)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(algorithms_list, rotation=45, ha='right')
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')

    # Add value labels on bars
    for i, v in enumerate(avg_comp):
        ax1.text(i, v, f'{v:,.0f}', ha='center', va='bottom', fontweight='bold')

    # Swaps for size 1000
    avg_swaps = size_1000['Avg_Swaps'].tolist()
    min_swaps = size_1000['Min_Swaps'].tolist()
    max_swaps = size_1000['Max_Swaps'].tolist()

    bars2 = ax2.bar(x_pos, avg_swaps, alpha=0.8, 
                    color=[color_map[algo] for algo in algorithms_list])

    # Add error bars
    yerr_swaps = [np.array(avg_swaps) - np.array(min_swaps), 
                  np.array(max_swaps) - np.array(avg_swaps)]
    ax2.errorbar(x_pos, avg_swaps, yerr=yerr_swaps, fmt='none', capsize=5, capthick=2, color='black')

    ax2.set_xlabel('Sorting Algorithm', fontsize=12)
    ax2.set_ylabel('Number of Swaps', fontsize=12)
    ax2.set_title('Swaps for Array Size 1000\n(with Min-Max Range)', fontsize=14)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(algorithms_list, rotation=45, ha='right')
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')

    # Add value labels on bars
    for i, v in enumerate(avg_swaps):
        ax2.text(i, v, f'{v:,.0f}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig('size_1000_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: size_1000_analysis.png")
    plt.show()

    # Figure 4: Combined Comparisons and Swaps in one plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Top plot: Comparisons
    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        ax1.plot(algo_data['Size'], algo_data['Avg_Comparisons'], 
                marker='o', linewidth=3, markersize=6, label=algo, color=color_map[algo])

    ax1.set_ylabel('Average Comparisons (log scale)', fontsize=12)
    ax1.set_title('Sorting Algorithm Performance Analysis', fontsize=16, fontweight='bold')
    ax1.legend(fontsize=10, loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')

    # Bottom plot: Swaps
    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        ax2.plot(algo_data['Size'], algo_data['Avg_Swaps'], 
                marker='s', linewidth=3, markersize=6, label=algo, color=color_map[algo])

    ax2.set_xlabel('Array Size', fontsize=12)
    ax2.set_ylabel('Average Swaps (log scale)', fontsize=12)
    ax2.legend(fontsize=10, loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')

    plt.tight_layout()
    plt.savefig('combined_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: combined_analysis.png")
    plt.show()

    # Figure 5: Algorithm Efficiency (Total Operations per Element)
    plt.figure(figsize=(12, 8))

    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        total_ops = algo_data['Avg_Comparisons'] + algo_data['Avg_Swaps']
        efficiency = total_ops / algo_data['Size']
        plt.plot(algo_data['Size'], efficiency, 
                marker='d', linewidth=3, markersize=8, 
                label=f'{algo}', color=color_map[algo])

    plt.xlabel('Array Size', fontsize=14)
    plt.ylabel('Total Operations per Element', fontsize=14)
    plt.title('Algorithm Efficiency: Total Operations per Element', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('efficiency_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: efficiency_analysis.png")
    plt.show()

    # Define theoretical complexities for normalization
    def get_complexity_factor(algorithm, n):
        """Get the theoretical complexity factor for normalization"""
        if algorithm in ['Bubble Sort', 'Selection Sort', 'Insertion Sort']:
            return n * n  # O(n²)
        elif algorithm in ['Merge Sort', 'Quick Sort', 'Heap Sort']:
            return n * np.log2(n)  # O(n log n)
        else:
            return n * n  # Default to O(n²)

    # Figure 6: Normalized Comparisons (divided by theoretical complexity)
    plt.figure(figsize=(14, 8))

    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        normalized_comparisons = []
        
        for _, row in algo_data.iterrows():
            n = row['Size']
            comparisons = row['Avg_Comparisons']
            complexity_factor = get_complexity_factor(algo, n)
            normalized = comparisons / complexity_factor
            normalized_comparisons.append(normalized)
        
        plt.plot(algo_data['Size'], normalized_comparisons, 
                marker='o', linewidth=3, markersize=8, label=algo, color=color_map[algo])

    plt.xlabel('Array Size (n)', fontsize=14)
    plt.ylabel('Normalized Comparisons (Comparisons / Theoretical Complexity)', fontsize=14)
    plt.title('Normalized Algorithm Performance: Comparisons / Time Complexity', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('normalized_comparisons.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: normalized_comparisons.png")
    plt.show()

    # Figure 7: Normalized Swaps (divided by theoretical complexity)
    plt.figure(figsize=(14, 8))

    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        normalized_swaps = []
        
        for _, row in algo_data.iterrows():
            n = row['Size']
            swaps = row['Avg_Swaps']
            complexity_factor = get_complexity_factor(algo, n)
            normalized = swaps / complexity_factor
            normalized_swaps.append(normalized)
        
        plt.plot(algo_data['Size'], normalized_swaps, 
                marker='s', linewidth=3, markersize=8, label=algo, color=color_map[algo])

    plt.xlabel('Array Size (n)', fontsize=14)
    plt.ylabel('Normalized Swaps (Swaps / Theoretical Complexity)', fontsize=14)
    plt.title('Normalized Algorithm Performance: Swaps / Time Complexity', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('normalized_swaps.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: normalized_swaps.png")
    plt.show()

    # Figure 8: Combined Normalized Analysis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))

    # Top plot: Normalized Comparisons
    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        normalized_comparisons = []
        
        for _, row in algo_data.iterrows():
            n = row['Size']
            comparisons = row['Avg_Comparisons']
            complexity_factor = get_complexity_factor(algo, n)
            normalized = comparisons / complexity_factor
            normalized_comparisons.append(normalized)
        
        ax1.plot(algo_data['Size'], normalized_comparisons, 
                marker='o', linewidth=3, markersize=6, label=algo, color=color_map[algo])

    ax1.set_ylabel('Normalized Comparisons\n(Comparisons / Theoretical Complexity)', fontsize=12)
    ax1.set_title('Normalized Algorithm Performance Analysis', fontsize=16, fontweight='bold')
    ax1.legend(fontsize=11, loc='upper right')
    ax1.grid(True, alpha=0.3)

    # Bottom plot: Normalized Swaps
    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        normalized_swaps = []
        
        for _, row in algo_data.iterrows():
            n = row['Size']
            swaps = row['Avg_Swaps']
            complexity_factor = get_complexity_factor(algo, n)
            normalized = swaps / complexity_factor
            normalized_swaps.append(normalized)
        
        ax2.plot(algo_data['Size'], normalized_swaps, 
                marker='s', linewidth=3, markersize=6, label=algo, color=color_map[algo])

    ax2.set_xlabel('Array Size (n)', fontsize=12)
    ax2.set_ylabel('Normalized Swaps\n(Swaps / Theoretical Complexity)', fontsize=12)
    ax2.legend(fontsize=11, loc='upper right')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('combined_normalized_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: combined_normalized_analysis.png")
    plt.show()

    # Figure 9: Normalized Total Operations
    plt.figure(figsize=(14, 8))

    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        normalized_total = []
        
        for _, row in algo_data.iterrows():
            n = row['Size']
            total_ops = row['Avg_Comparisons'] + row['Avg_Swaps']
            complexity_factor = get_complexity_factor(algo, n)
            normalized = total_ops / complexity_factor
            normalized_total.append(normalized)
        
        plt.plot(algo_data['Size'], normalized_total, 
                marker='d', linewidth=3, markersize=8, label=algo, color=color_map[algo])

    plt.xlabel('Array Size (n)', fontsize=14)
    plt.ylabel('Normalized Total Operations\n(Total Operations / Theoretical Complexity)', fontsize=14)
    plt.title('Normalized Total Operations: (Comparisons + Swaps) / Time Complexity', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('normalized_total_operations.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: normalized_total_operations.png")
    plt.show()

    # Print detailed analysis
    print("\n" + "="*70)
    print("DETAILED PERFORMANCE ANALYSIS")
    print("="*70)

    # Analysis for different array sizes
    for size in [100, 500, 1000]:
        size_data = df[df['Size'] == size].copy()
        
        print(f"\n📊 ARRAY SIZE {size}:")
        print("-" * 40)
        
        # Sort by comparisons
        size_data_comp = size_data.sort_values('Avg_Comparisons')
        print("🔍 COMPARISONS (Best → Worst):")
        for i, (_, row) in enumerate(size_data_comp.iterrows(), 1):
            print(f"  {i}. {row['Algorithm']:15} - {row['Avg_Comparisons']:8,.0f} comparisons")
        
        # Sort by swaps
        size_data_swaps = size_data.sort_values('Avg_Swaps')
        print("\n🔄 SWAPS (Best → Worst):")
        for i, (_, row) in enumerate(size_data_swaps.iterrows(), 1):
            print(f"  {i}. {row['Algorithm']:15} - {row['Avg_Swaps']:8,.0f} swaps")

    # Overall efficiency ranking
    print(f"\n🏆 OVERALL EFFICIENCY RANKING (for size 1000):")
    print("-" * 50)
    size_1000 = df[df['Size'] == 1000].copy()
    size_1000['Total_Ops'] = size_1000['Avg_Comparisons'] + size_1000['Avg_Swaps']
    size_1000_sorted = size_1000.sort_values('Total_Ops')

    for i, (_, row) in enumerate(size_1000_sorted.iterrows(), 1):
        total_ops = row['Total_Ops']
        print(f"  {i}. {row['Algorithm']:15} - {total_ops:8,.0f} total operations")

    # Normalization Analysis
    print(f"\n📊 NORMALIZATION ANALYSIS (Actual vs Theoretical Performance):")
    print("-" * 60)
    print("Lower values = better performance relative to theoretical complexity")
    print()

    for size in [1000]:  # Focus on largest size for clearest comparison
        size_data = df[df['Size'] == size].copy()
        print(f"Array Size {size} - Normalized Values:")
        print("(Actual Operations ÷ Theoretical Complexity)")
        print()
        
        normalization_results = []
        for _, row in size_data.iterrows():
            algo = row['Algorithm']
            n = row['Size']
            comparisons = row['Avg_Comparisons']
            swaps = row['Avg_Swaps']
            total_ops = comparisons + swaps
            
            # Calculate theoretical complexity factor
            if algo in ['Bubble Sort', 'Selection Sort', 'Insertion Sort']:
                complexity_factor = n * n  # O(n²)
                complexity_name = "O(n²)"
            else:  # Merge Sort, Quick Sort, Heap Sort
                complexity_factor = n * np.log2(n)  # O(n log n)
                complexity_name = "O(n log n)"
            
            normalized_total = total_ops / complexity_factor
            normalization_results.append({
                'Algorithm': algo,
                'Complexity': complexity_name,
                'Normalized_Value': normalized_total,
                'Total_Operations': total_ops
            })
        
        # Sort by normalized value
        normalization_results.sort(key=lambda x: x['Normalized_Value'])
        
        for i, result in enumerate(normalization_results, 1):
            print(f"  {i}. {result['Algorithm']:15} ({result['Complexity']:10}) - "
                  f"Normalized: {result['Normalized_Value']:6.2f}")

    print(f"\n{'='*70}")
    print("📈 ALL GRAPHS GENERATED:")
    print("  ✓ comparisons_vs_size.png")
    print("  ✓ swaps_vs_size.png") 
    print("  ✓ size_1000_analysis.png")
    print("  ✓ combined_analysis.png")
    print("  ✓ efficiency_analysis.png")
    print("  ✓ normalized_comparisons.png")
    print("  ✓ normalized_swaps.png")
    print("  ✓ combined_normalized_analysis.png")
    print("  ✓ normalized_total_operations.png")
    print(f"{'='*70}")

    print("\n🎯 KEY INSIGHTS:")
    print("• Merge Sort: Most efficient O(n log n) algorithm")
    print("• Quick Sort: Fast but variable performance")
    print("• Heap Sort: Consistent O(n log n) performance")
    print("• Insertion Sort: Good for small arrays")
    print("• Selection Sort: Fewer swaps than Bubble Sort")
    print("• Bubble Sort: Least efficient but simple to understand")

    print("\n📊 NORMALIZATION INSIGHTS:")
    print("• Normalized graphs show how algorithms perform relative to their theoretical complexity")
    print("• Lower normalized values = better implementation efficiency")
    print("• O(n log n) algorithms should have relatively flat normalized curves")
    print("• O(n²) algorithms may show variation due to implementation details")
    print("• Normalized analysis helps identify algorithms that outperform their theoretical bounds")
if __name__ == "__main__":
    try:
        create_plots()
    except ImportError as e:
        print(f"Error: Missing required Python package.")
        print("Please install required packages:")
        print("pip install matplotlib pandas numpy")
        print(f"\nSpecific error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure 'detailed_results.csv' exists in the current directory.")
