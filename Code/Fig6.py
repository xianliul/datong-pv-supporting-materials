import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# ================= Global Settings =================
# Set font to Times New Roman for academic publication
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

# File path provided in your prompt
file_path = r'E:\Annual_Ecological_Stats_ASF_B2000.csv'

# Load data
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: CSV file not found at {file_path}. Please check the path.")
    exit()

# Configuration for the four plots with Fig 6a-d prefix
# Ordered as requested: Albedo (a), LST (b), SMMI (c), NDVI (d)
plot_configs = [
    {
        'id': 'Fig. 6a',
        'name': 'Albedo',
        'mean_col': 'Albedo_mean_mean',
        'std_col': 'Albedo_stdDev',
        'ylabel': 'Albedo',
        'ylim': (0.05, 0.25),
        'major_y': 0.05,
        'minor_y': 0.025
    },
    {
        'id': 'Fig. 6b',
        'name': 'LST',
        'mean_col': 'LST_mean_mean',
        'std_col': 'LST_stdDev',
        'ylabel': 'LST (℃)',
        'ylim': (10, 30),
        'major_y': 5.0,
        'minor_y': 2.5
    },
    {
        'id': 'Fig. 6c',
        'name': 'SMMI',
        'mean_col': 'SMMI_mean_mean',
        'std_col': 'SMMI_stdDev',
        'ylabel': 'SMMI',
        'ylim': (0.35, 0.6),
        'major_y': 0.05,
        'minor_y': 0.025
    },
    {
        'id': 'Fig. 6d',
        'name': 'NDVI',
        'mean_col': 'NDVI_mean_mean',
        'std_col': 'NDVI_stdDev',
        'ylabel': 'NDVI',
        'ylim': (0.1, 0.45),
        'major_y': 0.1,
        'minor_y': 0.05
    }
]

# Region labels and colors
groups = {
    'ASF': {'label': 'PSF', 'color': '#d62728'},
    'B_2000': {'label': 'Surrounding Area', 'color': '#1f77b4'}
}

color_grid = '#808080'
color_const = '#383838'

# ================= Plotting Loop =================
for config in plot_configs:
    # Set consistent figure size for all subplots
    fig, ax = plt.subplots(figsize=(10, 6))

    # 1. Construction period markers (2015-2016)
    ax.axvline(2015, color=color_const, linestyle='--', linewidth=1.2, zorder=1)
    ax.axvline(2016, color=color_const, linestyle='--', linewidth=1.2, zorder=1)

    # 2. Plot lines and uncertainty bands for each group
    for idd, grp in groups.items():
        subset = df[df['IDD'] == idd].sort_values('Year')
        years = subset['Year']
        means = subset[config['mean_col']]
        stds = subset[config['std_col']]

        # Main trend line
        ax.plot(years, means, label=grp['label'], color=grp['color'],
                marker='o', markersize=7, linewidth=2.0, zorder=3)

        # Shaded error band (Spatial heterogeneity)
        ax.fill_between(years, means - stds, means + stds,
                        color=grp['color'], alpha=0.1, zorder=2)

    # 3. Formatting Axes
    ax.set_ylim(config['ylim'])
    ax.set_xlim(2007.5, 2023.5)

    # Labeling
    # ax.set_xlabel('Year', fontsize=20, fontweight='bold')
    ax.set_ylabel(config['ylabel'], fontsize=22, fontweight='bold')

    # Title combining Figure ID and Parameter Name
    # ax.set_title(f"{config['id']} {config['name']}", fontsize=24, fontweight='bold', loc='left', pad=15)

    # 4. Grid and Legend
    ax.grid(True, which='major', linestyle='--', color=color_grid, alpha=0.4, linewidth=0.8)
    ax.legend(fontsize=22, loc='upper left', frameon=False)

    # 5. Tick Management
    # X-axis: Every 2 years major, 1 year minor
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

    # Y-axis: Custom locators from config
    ax.yaxis.set_major_locator(ticker.MultipleLocator(config['major_y']))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(config['minor_y']))

    # Tick style
    ax.tick_params(axis='both', which='major', labelsize=20, length=6, width=1.5)
    ax.tick_params(axis='both', which='minor', length=3, width=1.0)

    # 6. Final Save
    save_filename = f"{config['id'].replace('.', '').replace(' ', '_')}_{config['name']}_Trend.png"
    plt.savefig(save_filename, dpi=500, bbox_inches='tight')
    print(f"Successfully generated: {save_filename}")
    plt.close()





'''Fig 6e'''
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ================= 1. Environment and Font Settings =================
# Set font to Times New Roman for academic publication
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

# Data Preparation
periods = ['Annual', 'Spring', 'Summer', 'Autumn', 'Winter']
data_rates = {
    'Albedo': [-7.26, -5.19, -7.00, -9.59, -8.06],
    'SMMI': [-3.82, -2.98, -3.60, -4.99, -3.96],
    'NDVI': [-6.93, -7.89, -3.90, -8.41, -11.76]
}
data_lst = [-0.9960, -1.6630, -0.05, -0.3088, -1.9669]

# ================= 2. Color and Transparency Configuration =================
colors_academic = {
    'Albedo': '#7F7F7F', # Academic Grey
    'SMMI': '#DD8452',   # Muted Earth
    'NDVI': '#55A868',   # Soft Green
    'LST': '#C44E52'     # Coral Red
}
bar_alpha = 0.7 # 30% Transparency

# ================= 3. Create Canvas (20:5 Aspect Ratio) =================
fig, ax1 = plt.subplots(figsize=(20, 5))
x = np.arange(len(periods))
width = 0.2

# ================= 4. Plot Bar Charts =================
r1 = ax1.bar(x - 1.2*width, data_rates['Albedo'], width,
             label=r'$\Delta$Albedo (%)', color=colors_academic['Albedo'],
             edgecolor='black', linewidth=0.8, alpha=bar_alpha)
r2 = ax1.bar(x - 0.2*width, data_rates['SMMI'], width,
             label=r'$\Delta$SMMI (%)', color=colors_academic['SMMI'],
             edgecolor='black', linewidth=0.8, alpha=bar_alpha)
r3 = ax1.bar(x + 0.8*width, data_rates['NDVI'], width,
             label=r'$\Delta$NDVI (%)', color=colors_academic['NDVI'],
             edgecolor='black', linewidth=0.8, alpha=bar_alpha)

# Secondary Axis (LST)
ax2 = ax1.twinx()
r4 = ax2.bar(x + 1.8*width, data_lst, width*0.8,
             label=r'$\Delta$LST (℃)', color=colors_academic['LST'],
             edgecolor='black', linewidth=0.8, alpha=bar_alpha)

# ================= 5. Ranges and Zero Line (0 at Top) =================
ax1.set_ylim(-14, 0)
ax2.set_ylim(-2.5, 0)
# Highlight zero baseline
ax1.axhline(0, color='black', linewidth=3, zorder=10)

# ================= 6. Labels and Font Sizes =================
label_size = 26
tick_size = 22
value_size = 22

ax1.set_xlabel('Period', fontsize=label_size, fontweight='bold')
ax1.set_ylabel('Change rate (%)', fontsize=label_size, fontweight='bold')
ax2.set_ylabel(r'$\Delta$LST (℃)', fontsize=label_size, fontweight='bold', color=colors_academic['LST'])

ax1.set_xticks(x)
ax1.set_xticklabels(periods, fontsize=tick_size, fontweight='bold')

# ================= 7. Numerical Annotation (One Decimal Place) =================
def autolabel_one_decimal(rects, ax, color='black', offset=8):
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, -offset), textcoords="offset points",
                    ha='center', va='top', fontsize=value_size, fontweight='bold', color=color)

autolabel_one_decimal(r1, ax1)
autolabel_one_decimal(r2, ax1)
autolabel_one_decimal(r3, ax1)
autolabel_one_decimal(r4, ax2, color=colors_academic['LST'])

# ================= 8. Aesthetic Refinement =================
# Set outer border (spines) to be thinner (1.0 instead of 2.0)
for ax in [ax1, ax2]:
    for spine in ax.spines.values():
        spine.set_linewidth(1.0) # Thinned outer border
        spine.set_zorder(100)

ax1.grid(True, axis='y', linestyle='--', color='#808080', alpha=0.3)

# Legend Configuration: 4 Columns
ax1.legend(handles=[r1, r2, r3, r4], labels=[h.get_label() for h in [r1, r2, r3, r4]],
           fontsize=22, loc='lower left', frameon=False, ncol=4)

ax1.tick_params(axis='both', which='major', labelsize=tick_size, length=8, width=1.5)
ax2.tick_params(axis='y', labelsize=tick_size, labelcolor=colors_academic['LST'], length=8, width=1.5)

# Add Minor Ticks
ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

plt.tight_layout()
plt.savefig('Fig6e_Ecological_Impact_Summary.png', dpi=500)
print("Successfully generated: Fig_6e.png")
# plt.show()
print("\nAll processing tasks completed successfully.")