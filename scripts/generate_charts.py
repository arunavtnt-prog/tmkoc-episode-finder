#!/usr/bin/env python3
"""
Generate modern, visually striking financial charts.
Anthropic-inspired with gradient colors and clean design.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
from pathlib import Path
import numpy as np

# Modern color palette
COLORS = {
    'primary_blue': '#007BFF',
    'light_blue': '#00D4FF',
    'navy': '#0B0E14',
    'grey': '#5B5E63',
    'bg': '#F8F9FB',
    'white': '#FFFFFF'
}

# Configure matplotlib for modern output
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'DejaVu Sans', 'Arial']
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 18
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.edgecolor'] = COLORS['grey']
plt.rcParams['xtick.color'] = COLORS['grey']
plt.rcParams['ytick.color'] = COLORS['grey']
plt.rcParams['text.color'] = COLORS['navy']
plt.rcParams['axes.facecolor'] = COLORS['white']
plt.rcParams['figure.facecolor'] = COLORS['white']

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

def add_gradient_background(ax, color1, color2):
    """Add subtle gradient background."""
    gradient = np.linspace(0, 1, 256).reshape(256, 1)
    gradient = np.hstack((gradient, gradient))
    ax.imshow(gradient, extent=[ax.get_xlim()[0], ax.get_xlim()[1],
                                 ax.get_ylim()[0], ax.get_ylim()[1]],
              aspect='auto', cmap=plt.cm.Blues, alpha=0.03, zorder=0)

def generate_revenue_forecast(df, output_dir):
    """Generate modern revenue forecast with gradient bars."""
    fig, ax1 = plt.subplots(figsize=(12, 6), facecolor=COLORS['white'])
    fig.patch.set_facecolor(COLORS['white'])

    x = np.arange(len(df))
    quarters = create_quarter_labels(df)

    # Create gradient bars
    bars = ax1.bar(x, df['Revenue'], width=0.6, color=COLORS['primary_blue'],
                   alpha=0.85, edgecolor=COLORS['light_blue'], linewidth=2, zorder=3)

    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, df['Revenue'])):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height + df['Revenue'].max()*0.02,
                format_currency(val, None),
                ha='center', va='bottom', fontsize=9, fontweight='bold',
                color=COLORS['navy'])

    ax1.set_xlabel('Quarter', fontweight='bold', color=COLORS['navy'], fontsize=13)
    ax1.set_ylabel('Revenue', fontweight='bold', color=COLORS['primary_blue'], fontsize=13)
    ax1.tick_params(axis='y', labelcolor=COLORS['primary_blue'])
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(format_currency))

    # Customer line on secondary axis
    ax2 = ax1.twinx()
    line = ax2.plot(x, df['Customers'], color=COLORS['light_blue'], marker='o',
                    linewidth=3.5, markersize=8, label='Customers',
                    markerfacecolor=COLORS['light_blue'],
                    markeredgecolor=COLORS['white'], markeredgewidth=2, zorder=4)
    ax2.set_ylabel('Customers', fontweight='bold', color=COLORS['light_blue'], fontsize=13)
    ax2.tick_params(axis='y', labelcolor=COLORS['light_blue'])
    ax2.spines['right'].set_visible(False)

    # X-axis
    ax1.set_xticks(x)
    ax1.set_xticklabels(quarters, fontsize=10, color=COLORS['grey'])

    # Title with styled box
    title_text = 'Revenue Growth & Customer Acquisition'
    ax1.text(0.5, 1.08, title_text, transform=ax1.transAxes,
            fontsize=18, fontweight='bold', ha='center', color=COLORS['navy'])

    # Subtitle
    ax1.text(0.5, 1.03, '18x growth in 3 years', transform=ax1.transAxes,
            fontsize=12, ha='center', color=COLORS['grey'], style='italic')

    # Grid
    ax1.grid(axis='y', alpha=0.15, linestyle='-', color=COLORS['grey'], linewidth=0.8, zorder=1)
    ax1.set_axisbelow(True)

    # Legend with custom styling
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS['primary_blue'], alpha=0.85,
              edgecolor=COLORS['light_blue'], linewidth=2, label='Quarterly Revenue'),
        plt.Line2D([0], [0], color=COLORS['light_blue'], linewidth=3.5,
                   marker='o', markersize=8, label='Total Customers')
    ]
    ax1.legend(handles=legend_elements, loc='upper left', frameon=True,
              fancybox=True, shadow=True, fontsize=11)

    plt.tight_layout()
    plt.savefig(output_dir / 'revenue_forecast.pdf', dpi=300, bbox_inches='tight',
                facecolor=COLORS['white'])
    plt.savefig(output_dir / 'revenue_forecast.svg', dpi=300, bbox_inches='tight',
                facecolor=COLORS['white'])
    plt.close()

    print(f"✓ Generated revenue_forecast chart (modern design)")

def generate_expense_breakdown(df, output_dir):
    """Generate modern expense breakdown with profit emphasis."""
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=COLORS['white'])
    fig.patch.set_facecolor(COLORS['white'])

    x = np.arange(len(df))
    quarters = create_quarter_labels(df)
    width = 0.35

    # Bars with gradient effect
    bars1 = ax.bar(x - width/2, df['Revenue'], width,
                   color=COLORS['primary_blue'], alpha=0.85,
                   edgecolor=COLORS['light_blue'], linewidth=2, label='Revenue', zorder=3)
    bars2 = ax.bar(x + width/2, df['Expenses'], width,
                   color=COLORS['grey'], alpha=0.6,
                   edgecolor=COLORS['navy'], linewidth=2, label='Expenses', zorder=3)

    # Profit line
    profit = df['Revenue'] - df['Expenses']
    ax2 = ax.twinx()

    # Fill area for profit
    ax2.fill_between(x, 0, profit, alpha=0.15, color=COLORS['light_blue'], zorder=1)

    line = ax2.plot(x, profit, color=COLORS['light_blue'], marker='D',
                    linewidth=4, markersize=9, label='Net Profit',
                    markerfacecolor=COLORS['light_blue'],
                    markeredgecolor=COLORS['white'], markeredgewidth=2, zorder=4)

    # Zero line
    ax2.axhline(y=0, color=COLORS['navy'], linestyle='--', linewidth=1.5, alpha=0.5, zorder=2)

    # Breakeven annotation
    breakeven_idx = next((i for i, p in enumerate(profit) if p > 0), None)
    if breakeven_idx:
        ax2.annotate('Breakeven\nAchieved',
                    xy=(breakeven_idx, profit.iloc[breakeven_idx]),
                    xytext=(breakeven_idx-1, profit.iloc[breakeven_idx]+500000),
                    bbox=dict(boxstyle='round,pad=0.7', fc=COLORS['light_blue'],
                             ec=COLORS['primary_blue'], alpha=0.9, linewidth=2),
                    arrowprops=dict(arrowstyle='->', color=COLORS['primary_blue'], lw=2),
                    fontsize=10, fontweight='bold', color=COLORS['white'], ha='center')

    ax2.set_ylabel('Net Profit', fontweight='bold', color=COLORS['light_blue'], fontsize=13)
    ax2.tick_params(axis='y', labelcolor=COLORS['light_blue'])
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(format_currency))
    ax2.spines['right'].set_visible(False)

    # Labels
    ax.set_xlabel('Quarter', fontweight='bold', color=COLORS['navy'], fontsize=13)
    ax.set_ylabel('Amount', fontweight='bold', color=COLORS['navy'], fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(quarters, fontsize=10, color=COLORS['grey'])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_currency))

    # Title
    ax.text(0.5, 1.08, 'Financial Performance Overview', transform=ax.transAxes,
            fontsize=18, fontweight='bold', ha='center', color=COLORS['navy'])
    ax.text(0.5, 1.03, 'Revenue, Expenses & Path to Profitability',
            transform=ax.transAxes, fontsize=12, ha='center',
            color=COLORS['grey'], style='italic')

    # Grid
    ax.grid(axis='y', alpha=0.15, linestyle='-', color=COLORS['grey'], linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS['primary_blue'], alpha=0.85,
              edgecolor=COLORS['light_blue'], linewidth=2, label='Revenue'),
        Patch(facecolor=COLORS['grey'], alpha=0.6,
              edgecolor=COLORS['navy'], linewidth=2, label='Expenses'),
        plt.Line2D([0], [0], color=COLORS['light_blue'], linewidth=4,
                   marker='D', markersize=9, label='Net Profit')
    ]
    ax.legend(handles=legend_elements, loc='upper left', frameon=True,
             fancybox=True, shadow=True, fontsize=11)

    plt.tight_layout()
    plt.savefig(output_dir / 'expense_breakdown.pdf', dpi=300, bbox_inches='tight',
                facecolor=COLORS['white'])
    plt.savefig(output_dir / 'expense_breakdown.svg', dpi=300, bbox_inches='tight',
                facecolor=COLORS['white'])
    plt.close()

    print(f"✓ Generated expense_breakdown chart (modern design)")

def generate_arr_growth(df, output_dir):
    """Generate modern ARR growth with milestone emphasis."""
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=COLORS['white'])
    fig.patch.set_facecolor(COLORS['white'])

    x = np.arange(len(df))
    quarters = create_quarter_labels(df)

    # Gradient fill
    ax.fill_between(x, 0, df['ARR'], alpha=0.25,
                     color=COLORS['primary_blue'], zorder=1)
    ax.plot(x, df['ARR'], color=COLORS['primary_blue'], marker='o',
            linewidth=4, markersize=10, markerfacecolor=COLORS['light_blue'],
            markeredgecolor=COLORS['white'], markeredgewidth=3, label='ARR', zorder=3)

    # Milestone markers
    milestones = [
        (3, 'Break $1M ARR', df.iloc[3]['ARR']),
        (7, 'Break $10M ARR', df.iloc[7]['ARR']),
        (11, 'Break $50M ARR', df.iloc[11]['ARR'])
    ]

    for idx, label, value in milestones:
        if idx < len(df):
            # Draw milestone marker
            ax.plot(idx, value, 'D', markersize=15,
                   color=COLORS['light_blue'], markeredgecolor=COLORS['white'],
                   markeredgewidth=3, zorder=4)

            # Annotation with styled box
            ax.annotate(label, xy=(idx, value),
                       xytext=(15, 25), textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.8', fc=COLORS['primary_blue'],
                                ec=COLORS['light_blue'], alpha=0.95, linewidth=2.5),
                       arrowprops=dict(arrowstyle='->', color=COLORS['light_blue'],
                                      lw=2.5, connectionstyle='arc3,rad=0.3'),
                       fontsize=10, fontweight='bold', color=COLORS['white'])

    # Labels
    ax.set_xlabel('Quarter', fontweight='bold', color=COLORS['navy'], fontsize=13)
    ax.set_ylabel('Annual Recurring Revenue (ARR)', fontweight='bold',
                  color=COLORS['navy'], fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(quarters, fontsize=10, color=COLORS['grey'])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_currency))

    # Title
    ax.text(0.5, 1.08, 'ARR Growth Trajectory', transform=ax.transAxes,
            fontsize=18, fontweight='bold', ha='center', color=COLORS['navy'])
    ax.text(0.5, 1.03, 'On track to $50M+ ARR by Q4 2027',
            transform=ax.transAxes, fontsize=12, ha='center',
            color=COLORS['grey'], style='italic')

    # Grid
    ax.grid(axis='y', alpha=0.15, linestyle='-', color=COLORS['grey'],
            linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(output_dir / 'arr_growth.pdf', dpi=300, bbox_inches='tight',
                facecolor=COLORS['white'])
    plt.savefig(output_dir / 'arr_growth.svg', dpi=300, bbox_inches='tight',
                facecolor=COLORS['white'])
    plt.close()

    print(f"✓ Generated arr_growth chart (modern design)")

def main():
    """Main function to generate all modern charts."""
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    data_file = project_dir / 'data' / 'forecast.csv'
    output_dir = project_dir / 'charts'

    output_dir.mkdir(exist_ok=True)

    print(f"Loading data from {data_file}...")
    df = pd.read_csv(data_file)

    print("Generating modern, visually striking charts...")
    generate_revenue_forecast(df, output_dir)
    generate_expense_breakdown(df, output_dir)
    generate_arr_growth(df, output_dir)

    print(f"\n✓ All modern charts generated in {output_dir}/")
    print(f"  Style: Modern, gradient-based, visually engaging")

if __name__ == '__main__':
    main()
