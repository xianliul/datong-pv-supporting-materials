import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Set font to Times New Roman
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = ['Times New Roman'] + matplotlib.rcParams['font.serif']

# Load data (adjust the path according to your actual environment)
file_path = r'E:\MODIS_GPP_Phenology.xlsx'
df = pd.read_excel(file_path, sheet_name="Sheet1")

# Filter data for the years 2008-2023
df = df[(df['year'] >= 2008) & (df['year'] <= 2023)]

# Group by IDD
psf = df[df['IDD'] == 'PSF'].sort_values('year')
ctrl = df[df['IDD'] == 'Ctrl'].sort_values('year')

# Ensure matching years for difference calculation
years = sorted(list(set(psf['year']) & set(ctrl['year'])))
psf = psf[psf['year'].isin(years)]
ctrl = ctrl[ctrl['year'].isin(years)]
diff_los = psf['GSL_mean'].values - ctrl['GSL_mean'].values

# Define color palette
color_eos = '#CC9900'
color_sos = '#00DC00'
color_diff = '#0000FF'
color_gpp = 'green'
color_ctrl_shadow = '#E0E0E0'

# [Modification]: Set height ratio to 1.5:1 using gridspec_kw
# Slightly increased figsize height (9 -> 11) to maintain subplot (b) proportions
fig, axes = plt.subplots(2, 1, figsize=(12, 11), constrained_layout=True,
                         gridspec_kw={'height_ratios': [1.5, 1]})

# Subplot (a): SOS, EOS, and delta GSL
ax1 = axes[0]
ax1_twin = ax1.twinx()

# Plot SOS (Start of Growing Season)
ax1.plot(psf['year'], psf['SOS_DOY_mean'], color=color_sos, label='SOGS_Photovoltaic Solar Farm', linestyle='-', marker='o', markersize=6)
ax1.fill_between(psf['year'], psf['SOS_DOY_mean'] - psf['SOS_DOY_stdDev'], psf['SOS_DOY_mean'] + psf['SOS_DOY_stdDev'], color=color_sos, alpha=0.15)
ax1.plot(ctrl['year'], ctrl['SOS_DOY_mean'], color=color_sos, label='SOGS_Control Area', linestyle='--', marker='o', mfc='none', markersize=6)
ax1.fill_between(ctrl['year'], ctrl['SOS_DOY_mean'] - ctrl['SOS_DOY_stdDev'], ctrl['SOS_DOY_mean'] + ctrl['SOS_DOY_stdDev'], color=color_ctrl_shadow, alpha=0.3)

# Plot EOS (End of Growing Season)
ax1.plot(psf['year'], psf['EOS_DOY_mean'], color=color_eos, label='EOGS_Photovoltaic Solar Farm', linestyle='-', marker='o', markersize=6)
ax1.fill_between(psf['year'], psf['EOS_DOY_mean'] - psf['EOS_DOY_stdDev'], psf['EOS_DOY_mean'] + psf['EOS_DOY_stdDev'], color=color_eos, alpha=0.4)
ax1.plot(ctrl['year'], ctrl['EOS_DOY_mean'], color=color_eos, label='EOGS_Control Area', linestyle='--', marker='o', mfc='none', markersize=6)
ax1.fill_between(ctrl['year'], ctrl['EOS_DOY_mean'] - ctrl['EOS_DOY_stdDev'], ctrl['EOS_DOY_mean'] + ctrl['EOS_DOY_stdDev'], color=color_ctrl_shadow, alpha=0.5)

# Plot delta GSL (Right axis)
ax1_twin.plot(years, diff_los, color=color_diff, label='$\Delta$LOGS (Photovoltaic - Control)', linestyle='-', marker='s', markersize=6)
ax1_twin.axhline(0, color='black', linestyle=':', linewidth=1)

# Axis alignment and formatting
ax1.set_ylim(90, 310)
ax1_twin.set_ylim(-25, 20)
ax1.set_ylabel('Day of Year (DOY)', fontsize=20, fontweight='bold')
ax1_twin.set_ylabel('Difference of LOGS (day)', fontsize=20, fontweight='bold')
ax1.tick_params(labelsize=20)
ax1_twin.tick_params(labelsize=20)
ax1.grid(True, linestyle=':', alpha=0.6)

# Label position for (a)
ax1.text(2009, 275, '(a)', fontsize=22, fontweight='bold', va='center', ha='center')

# Legend for Subplot (a)
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax1_twin.get_legend_handles_labels()
leg1 = ax1.legend(h1 + h2, l1 + l2, loc='center right', bbox_to_anchor=(0.99, 0.7), ncol=1, fontsize=16, frameon=True)
leg1.get_frame().set_facecolor('white')
leg1.get_frame().set_edgecolor('none')
leg1.get_frame().set_alpha(0.6)

# Subplot (b): GPP
ax2 = axes[1]
ax2.plot(psf['year'], psf['GPP_Annual_mean'], color=color_gpp, label='GPP_Photovoltaic Solar Farm', linestyle='-', marker='o', markersize=7)
ax2.fill_between(psf['year'], psf['GPP_Annual_mean'] - psf['GPP_Annual_stdDev'], psf['GPP_Annual_mean'] + psf['GPP_Annual_stdDev'], color=color_gpp, alpha=0.15)
ax2.plot(ctrl['year'], ctrl['GPP_Annual_mean'], color=color_gpp, label='GPP_Control Area', linestyle='--', marker='o', mfc='none', markersize=7)
ax2.fill_between(ctrl['year'], ctrl['GPP_Annual_mean'] - ctrl['GPP_Annual_stdDev'], ctrl['GPP_Annual_mean'] + ctrl['GPP_Annual_stdDev'], color=color_ctrl_shadow, alpha=0.3)

ax2.set_ylim(0.25, 0.6)
ax2.set_ylabel('GPP (kg C m$^{-2}$ yr$^{-1}$)', fontsize=20, fontweight='bold')
ax2.set_xlabel('Year', fontsize=20)
ax2.tick_params(labelsize=20)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='lower right', frameon=False, fontsize=16)

# Label position for (b)
ax2.text(2009, 0.55, '(b)', fontsize=22, fontweight='bold', va='center', ha='center')

# Reference lines for the construction period
for ax in [ax1, ax2]:
    ax.axvline(2015, color='gray', linewidth=1.2, linestyle='--', alpha=0.8)
    ax.axvline(2016, color='gray', linewidth=1.2, linestyle='--', alpha=0.8)
    ax.set_xticks(range(2008, 2024, 2))
    ax.set_xlim(2007.5, 2023.5)

plt.savefig('Fig10_GPP_Phenology_High_SubplotA.png', dpi=500)
plt.show()