import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def create_comprehensive_plots():
    """
    Create all comparison graphs including normalized analysis
    """
    # Check if the results file exists
    if not os.path.exists('detailed_results.csv'):
        print("Error: detailed_results.csv not found!")
        print("Please run the C program first to generate data.")
        return
    
    # Read the data
    df = pd.read_csv('detailed_results.csv')
    
    # Set up the plotting style
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (14, 10)
    plt.rcParams['font.size'] = 12
    
    # Get unique algorithms and sizes
    algorithms = df['Algorithm'].unique()
    sizes = sorted(df['Size'].unique())
    
    print(f"📊 Found data for algorithms: {', '.join(algorithms)}")
    print(f"📈 Array sizes: {sizes}")
    print("🎨 Generating comprehensive comparison graphs...\n")
    
    # Create color palette
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    color_map = {algo: colors[i] for i, algo in enumerate(algorithms)}
    
    # Define theoretical complexities for normalization
    def get_complexity_factor(algorithm, n):
        """Get the theoretical complexity factor for normalization"""
        if algorithm in ['Bubble Sort', 'Selection Sort', 'Insertion Sort']:
            return n * n  # O(n²)
        elif algorithm in ['Merge Sort', 'Quick Sort', 'Heap Sort']:
            return n * np.log2(n)  # O(n log n)
        else:
            return n * n  # Default to O(n²)

    # ===========================================
    # GRAPH 1: Regular Comparisons vs Array Size
    # ===========================================
    plt.figure(figsize=(14, 10))
    
    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        plt.plot(algo_data['Size'], algo_data['Avg_Comparisons'], 
                marker='o', linewidth=3, markersize=8, label=algo, color=color_map[algo])
    
    plt.xlabel('Array Size (n)', fontsize=14, fontweight='bold')
    plt.ylabel('Average Number of Comparisons', fontsize=14, fontweight='bold')
    plt.title('Sorting Algorithm Performance: Average Comparisons vs Array Size', 
              fontsize=16, fontweight='bold', pad=20)
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Log scale for better visibility
    
    # Add annotations for key insights
    plt.text(0.02, 0.98, 'Log Scale Used', transform=plt.gca().transAxes, 
             fontsize=10, verticalalignment='top', 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('plots/regular_comparisons_vs_size.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: plots/regular_comparisons_vs_size.png")
    plt.show()

    # ===========================================
    # GRAPH 2: Normalized Comparisons
    # ===========================================
    plt.figure(figsize=(14, 10))
    
    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        
        # Calculate normalized values
        normalized_comparisons = []
        for idx, row in algo_data.iterrows():
            complexity_factor = get_complexity_factor(row['Algorithm'], row['Size'])
            normalized_val = row['Avg_Comparisons'] / complexity_factor
            normalized_comparisons.append(normalized_val)
        
        plt.plot(algo_data['Size'], normalized_comparisons, 
                marker='s', linewidth=3, markersize=8, 
                label=f'{algo}', color=color_map[algo])
    
    plt.xlabel('Array Size (n)', fontsize=14, fontweight='bold')
    plt.ylabel('Normalized Comparisons (Comparisons / Theoretical Complexity)', 
               fontsize=14, fontweight='bold')
    plt.title('Normalized Algorithm Performance: Comparisons ÷ Theoretical Complexity', 
              fontsize=16, fontweight='bold', pad=20)
    plt.legend(fontsize=12, loc='upper right')
    plt.grid(True, alpha=0.3)
    
    # Add complexity annotations
    plt.text(0.02, 0.98, 'O(n²): Bubble, Selection, Insertion\nO(n log n): Merge, Quick, Heap', 
             transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('plots/normalized_comparisons_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: plots/normalized_comparisons_analysis.png")
    plt.show()

    # ===========================================
    # GRAPH 3: Side-by-Side Comparison
    # ===========================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Left plot: Regular comparisons
    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        ax1.plot(algo_data['Size'], algo_data['Avg_Comparisons'], 
                marker='o', linewidth=2.5, markersize=6, label=algo, color=color_map[algo])
    
    ax1.set_xlabel('Array Size (n)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Average Comparisons', fontsize=12, fontweight='bold')
    ax1.set_title('Regular Performance Analysis', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Right plot: Normalized comparisons
    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        
        normalized_comparisons = []
        for idx, row in algo_data.iterrows():
            complexity_factor = get_complexity_factor(row['Algorithm'], row['Size'])
            normalized_val = row['Avg_Comparisons'] / complexity_factor
            normalized_comparisons.append(normalized_val)
        
        ax2.plot(algo_data['Size'], normalized_comparisons, 
                marker='s', linewidth=2.5, markersize=6, 
                label=f'{algo}', color=color_map[algo])
    
    ax2.set_xlabel('Array Size (n)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Normalized Comparisons', fontsize=12, fontweight='bold')
    ax2.set_title('Normalized Performance Analysis', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Comprehensive Sorting Algorithm Comparison Analysis', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('plots/side_by_side_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: plots/side_by_side_comparison.png")
    plt.show()

    # ===========================================
    # GRAPH 4: Algorithm Efficiency Constants
    # ===========================================
    plt.figure(figsize=(14, 10))
    
    # Calculate average normalized values for each algorithm
    algo_constants = {}
    for algo in algorithms:
        algo_data = df[df['Algorithm'] == algo]
        normalized_values = []
        
        for idx, row in algo_data.iterrows():
            complexity_factor = get_complexity_factor(row['Algorithm'], row['Size'])
            normalized_val = row['Avg_Comparisons'] / complexity_factor
            normalized_values.append(normalized_val)
        
        algo_constants[algo] = np.mean(normalized_values)
    
    # Create bar chart
    algorithms_list = list(algo_constants.keys())
    constants_list = list(algo_constants.values())
    
    bars = plt.bar(algorithms_list, constants_list, 
                   color=[color_map[algo] for algo in algorithms_list], 
                   alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar, value in zip(bars, constants_list):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{value:.4f}', ha='center', va='bottom', fontweight='bold')
    
    plt.xlabel('Sorting Algorithms', fontsize=14, fontweight='bold')
    plt.ylabel('Average Constant Factor', fontsize=14, fontweight='bold')
    plt.title('Algorithm Efficiency: Average Constant Factors\n(Lower is Better)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add interpretation text
    plt.text(0.02, 0.98, 
             'Constant Factor = Actual Comparisons ÷ Theoretical Complexity\n' +
             'Shows how close each algorithm is to its theoretical performance',
             transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('plots/algorithm_efficiency_constants.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: plots/algorithm_efficiency_constants.png")
    plt.show()

    # ===========================================
    # GRAPH 5: Performance Trends Analysis
    # ===========================================
    plt.figure(figsize=(14, 10))
    
    # Focus on O(n log n) algorithms for detailed comparison
    nlogn_algorithms = ['Merge Sort', 'Quick Sort', 'Heap Sort']
    
    for algo in nlogn_algorithms:
        algo_data = df[df['Algorithm'] == algo]
        normalized_comparisons = []
        
        for idx, row in algo_data.iterrows():
            complexity_factor = get_complexity_factor(row['Algorithm'], row['Size'])
            normalized_val = row['Avg_Comparisons'] / complexity_factor
            normalized_comparisons.append(normalized_val)
        
        plt.plot(algo_data['Size'], normalized_comparisons, 
                marker='o', linewidth=4, markersize=10, 
                label=f'{algo}', color=color_map[algo])
    
    plt.xlabel('Array Size (n)', fontsize=14, fontweight='bold')
    plt.ylabel('Normalized Comparisons (Comparisons ÷ n log n)', 
               fontsize=14, fontweight='bold')
    plt.title('O(n log n) Algorithms: Detailed Efficiency Comparison', 
              fontsize=16, fontweight='bold', pad=20)
    plt.legend(fontsize=14, loc='upper right')
    plt.grid(True, alpha=0.3)
    
    # Add trend analysis
    plt.text(0.02, 0.98, 
             'Performance Insights:\n' +
             '• Lower values = more efficient\n' +
             '• Flatter lines = more consistent\n' +
             '• Shows which algorithm has best constant factor',
             transform=plt.gca().transAxes, fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('plots/nlogn_algorithms_detailed.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: plots/nlogn_algorithms_detailed.png")
    plt.show()

    # ===========================================
    # Summary Statistics
    # ===========================================
    print("\n" + "="*60)
    print("📊 COMPREHENSIVE ANALYSIS SUMMARY")
    print("="*60)
    
    print("\n🎯 Algorithm Efficiency Constants (Lower = Better):")
    for algo, constant in sorted(algo_constants.items(), key=lambda x: x[1]):
        print(f"   {algo:15s}: {constant:.6f}")
    
    print(f"\n🏆 Most Efficient Algorithm: {min(algo_constants, key=algo_constants.get)}")
    print(f"📈 Least Efficient Algorithm: {max(algo_constants, key=algo_constants.get)}")
    
    # Best and worst for size 1000
    size_1000_data = df[df['Size'] == 1000].sort_values('Avg_Comparisons')
    print(f"\n📊 For Array Size 1000:")
    print(f"   Best Performance:  {size_1000_data.iloc[0]['Algorithm']} ({size_1000_data.iloc[0]['Avg_Comparisons']:,} comparisons)")
    print(f"   Worst Performance: {size_1000_data.iloc[-1]['Algorithm']} ({size_1000_data.iloc[-1]['Avg_Comparisons']:,} comparisons)")
    
    print("\n" + "="*60)
    print("✅ All graphs generated successfully!")
    print("📁 Check the 'plots/' folder for all generated images")
    print("="*60)

if __name__ == "__main__":
    # Create plots directory if it doesn't exist
    os.makedirs('plots', exist_ok=True)
    
    try:
        create_comprehensive_plots()
    except ImportError as e:
        print(f"❌ Error: Missing required Python package.")
        print("📦 Please install required packages:")
        print("   pip install matplotlib pandas numpy")
        print(f"\n🔍 Specific error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("📄 Make sure 'detailed_results.csv' exists in the current directory.")
