#!/usr/bin/env python3
"""
Generate financial charts from forecast CSV data.
Outputs both SVG and PDF formats for LaTeX inclusion.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import numpy as np

# Anthropic-inspired color palette
COLORS = {
    'orange': '#E86C38',
    'dark_orange': '#BF4C21',
    'black': '#191919',
    'gray': '#5F5F5F',
    'light_gray': '#F5F5F5',
    'blue': '#2D6DA4'
}

# Configure matplotlib for professional output
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Arial', 'DejaVu Sans']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 14
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.edgecolor'] = COLORS['gray']
plt.rcParams['xtick.color'] = COLORS['gray']
plt.rcParams['ytick.color'] = COLORS['gray']
plt.rcParams['text.color'] = COLORS['black']

def format_currency(value, pos=None):
    """Format large numbers as currency with K/M suffix."""
    if value >= 1_000_000:
        return f'${value/1_000_000:.1f}M'
    elif value >= 1_000:
        return f'${value/1_000:.0f}K'
    else:
        return f'${value:.0f}'

def create_quarter_labels(df):
    """Create readable quarter labels."""
    return [f"{row['Quarter']}\n{row['Year']}" for _, row in df.iterrows()]

def generate_revenue_forecast(df, output_dir):
    """Generate revenue forecast chart with revenue and customer growth."""
    fig, ax1 = plt.subplots(figsize=(10, 5))

    x = np.arange(len(df))
    quarters = create_quarter_labels(df)

    # Revenue bars
    bars = ax1.bar(x, df['Revenue'], color=COLORS['orange'], alpha=0.8, label='Quarterly Revenue')
    ax1.set_xlabel('Quarter', fontweight='bold', color=COLORS['black'])
    ax1.set_ylabel('Revenue', fontweight='bold', color=COLORS['orange'])
    ax1.tick_params(axis='y', labelcolor=COLORS['orange'])
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(format_currency))

    # Customer line on secondary axis
    ax2 = ax1.twinx()
    line = ax2.plot(x, df['Customers'], color=COLORS['blue'], marker='o',
                    linewidth=2.5, markersize=6, label='Customers')
    ax2.set_ylabel('Number of Customers', fontweight='bold', color=COLORS['blue'])
    ax2.tick_params(axis='y', labelcolor=COLORS['blue'])
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(COLORS['gray'])

    # X-axis labels
    ax1.set_xticks(x)
    ax1.set_xticklabels(quarters, rotation=0, ha='center')

    # Title and grid
    ax1.set_title('Revenue Forecast & Customer Growth', fontweight='bold', pad=20)
    ax1.grid(axis='y', alpha=0.2, linestyle='--', color=COLORS['gray'])

    # Combined legend
    bars_patch = mpatches.Patch(color=COLORS['orange'], alpha=0.8, label='Quarterly Revenue')
    line_patch = mpatches.Patch(color=COLORS['blue'], label='Customers')
    ax1.legend(handles=[bars_patch, line_patch], loc='upper left', frameon=False)

    plt.tight_layout()

    # Save in both formats
    plt.savefig(output_dir / 'revenue_forecast.svg', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'revenue_forecast.pdf', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Generated revenue_forecast chart")

def generate_expense_breakdown(df, output_dir):
    """Generate expense breakdown showing expenses vs revenue."""
    fig, ax = plt.subplots(figsize=(10, 5))

    x = np.arange(len(df))
    quarters = create_quarter_labels(df)
    width = 0.35

    # Revenue and expense bars
    bars1 = ax.bar(x - width/2, df['Revenue'], width, color=COLORS['orange'],
                   alpha=0.9, label='Revenue')
    bars2 = ax.bar(x + width/2, df['Expenses'], width, color=COLORS['gray'],
                   alpha=0.7, label='Expenses')

    # Profit line
    profit = df['Revenue'] - df['Expenses']
    ax2 = ax.twinx()
    line = ax2.plot(x, profit, color=COLORS['dark_orange'], marker='s',
                    linewidth=2.5, markersize=6, label='Profit', linestyle='--')
    ax2.axhline(y=0, color=COLORS['black'], linestyle='-', linewidth=0.8, alpha=0.3)
    ax2.set_ylabel('Profit', fontweight='bold', color=COLORS['dark_orange'])
    ax2.tick_params(axis='y', labelcolor=COLORS['dark_orange'])
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(format_currency))
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(COLORS['gray'])

    # X-axis and labels
    ax.set_xlabel('Quarter', fontweight='bold', color=COLORS['black'])
    ax.set_ylabel('Amount', fontweight='bold', color=COLORS['black'])
    ax.set_xticks(x)
    ax.set_xticklabels(quarters, rotation=0, ha='center')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_currency))

    # Title and grid
    ax.set_title('Financial Overview: Revenue, Expenses & Profit', fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.2, linestyle='--', color=COLORS['gray'])

    # Combined legend
    bars1_patch = mpatches.Patch(color=COLORS['orange'], alpha=0.9, label='Revenue')
    bars2_patch = mpatches.Patch(color=COLORS['gray'], alpha=0.7, label='Expenses')
    line_patch = mpatches.Patch(color=COLORS['dark_orange'], label='Profit')
    ax.legend(handles=[bars1_patch, bars2_patch, line_patch], loc='upper left', frameon=False)

    plt.tight_layout()

    # Save in both formats
    plt.savefig(output_dir / 'expense_breakdown.svg', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'expense_breakdown.pdf', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Generated expense_breakdown chart")

def generate_arr_growth(df, output_dir):
    """Generate ARR growth trajectory chart."""
    fig, ax = plt.subplots(figsize=(10, 5))

    x = np.arange(len(df))
    quarters = create_quarter_labels(df)

    # ARR area chart
    ax.fill_between(x, 0, df['ARR'], color=COLORS['orange'], alpha=0.3)
    ax.plot(x, df['ARR'], color=COLORS['dark_orange'], marker='o',
            linewidth=3, markersize=7, label='ARR')

    # Milestone markers
    milestones = [(3, 'Break $1M'), (7, 'Break $10M'), (11, 'Break $50M')]
    for idx, label in milestones:
        if idx < len(df):
            ax.annotate(label, xy=(idx, df.iloc[idx]['ARR']),
                       xytext=(10, 20), textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.5', fc=COLORS['light_gray'],
                                ec=COLORS['orange'], alpha=0.9),
                       arrowprops=dict(arrowstyle='->', color=COLORS['orange'], lw=1.5),
                       fontsize=8, color=COLORS['black'], fontweight='bold')

    # Labels and formatting
    ax.set_xlabel('Quarter', fontweight='bold', color=COLORS['black'])
    ax.set_ylabel('Annual Recurring Revenue (ARR)', fontweight='bold', color=COLORS['black'])
    ax.set_xticks(x)
    ax.set_xticklabels(quarters, rotation=0, ha='center')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_currency))

    # Title and grid
    ax.set_title('ARR Growth Trajectory', fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.2, linestyle='--', color=COLORS['gray'])

    # Legend
    ax.legend(loc='upper left', frameon=False)

    plt.tight_layout()

    # Save in both formats
    plt.savefig(output_dir / 'arr_growth.svg', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'arr_growth.pdf', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Generated arr_growth chart")

def main():
    """Main function to generate all charts."""
    # Setup paths
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    data_file = project_dir / 'data' / 'forecast.csv'
    output_dir = project_dir / 'charts'

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Load data
    print(f"Loading data from {data_file}...")
    df = pd.read_csv(data_file)

    # Generate charts
    print("Generating charts...")
    generate_revenue_forecast(df, output_dir)
    generate_expense_breakdown(df, output_dir)
    generate_arr_growth(df, output_dir)

    print(f"\n✓ All charts generated successfully in {output_dir}/")
    print(f"  Formats: SVG (for web) and PDF (for LaTeX)")

if __name__ == '__main__':
    main()
