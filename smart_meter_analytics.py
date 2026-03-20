"""
Smart Meter Analytics — Energy Vending, Revenue Loss & Connectivity
====================================================================
Author: Opemipo Daniel Owolabi
Company: Deharyor Global Services Ltd
Project: Portfolio Project 5 — IoT Data Analytics & Revenue Intelligence
Tools: Python, Pandas, Matplotlib, Seaborn

Context:
--------
Deharyor Global Services Ltd installs and manages prepaid smart meters
across residential estates and military barracks in Lagos and Abuja.
Meters are imported from Turkey and connect via SIM card (GSM/GPRS),
transmitting transaction and connectivity data remotely.

The Nigerian Army is the company's largest client. Abuja clusters
consistently generate the highest revenue volume.

Cluster Areas:
--------------
LAGOS:  Pinnock Beach Estate, Ojo Barracks, Ikeja Cantonment
ABUJA:  Mogadishu Barracks, Mambiila Barracks, Niger Barracks,
        Ushafa Soldiers Camp, D'Mayors Estate, Defense Intelligence
        Agency (DIA), Army War College, Nigerian Navy Barracks

Business Questions Answered:
-----------------------------
  1. Cluster Performance    — which clusters vend most vs least
  2. Revenue Loss Detection — billed vs collected, leakage by cluster
  3. Inactive Meters        — meters with no vend in 30+ days
  4. Vending Patterns       — weekly transaction behaviour
  5. Abuja vs Lagos         — regional revenue comparison
  6. Connectivity Health    — online vs offline meters per cluster
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)

print("=" * 60)
print("  SMART METER ANALYTICS — DEHARYOR GLOBAL SERVICES LTD")
print("  Energy Vending & Revenue Intelligence")
print("  Analyst: Opemipo Daniel Owolabi")
print("=" * 60)


# ─────────────────────────────────────────────
# CLUSTER DATA
# Real cluster areas — Lagos and Abuja
# Abuja dominates in volume as per actual operations
# ─────────────────────────────────────────────

clusters = pd.DataFrame([
    # Lagos clusters
    {"Cluster": "Pinnock Beach Estate", "City": "Lagos", "Client_Type": "Private Estate",
     "Total_Meters": 320, "Active_Meters": 285, "Online_Meters": 271,
     "Monthly_Units_Billed": 48_500, "Monthly_Units_Vended": 41_200,
     "Amount_Billed": 12_850_000, "Amount_Collected": 10_920_000,
     "Inactive_30d": 35, "Avg_Vend_Amount": 8_500},

    {"Cluster": "Ojo Barracks",         "City": "Lagos", "Client_Type": "Military",
     "Total_Meters": 480, "Active_Meters": 420, "Online_Meters": 398,
     "Monthly_Units_Billed": 72_000, "Monthly_Units_Vended": 59_400,
     "Amount_Billed": 19_200_000, "Amount_Collected": 15_840_000,
     "Inactive_30d": 60, "Avg_Vend_Amount": 7_200},

    {"Cluster": "Ikeja Cantonment",     "City": "Lagos", "Client_Type": "Military",
     "Total_Meters": 560, "Active_Meters": 498, "Online_Meters": 471,
     "Monthly_Units_Billed": 84_000, "Monthly_Units_Vended": 71_400,
     "Amount_Billed": 22_400_000, "Amount_Collected": 19_040_000,
     "Inactive_30d": 62, "Avg_Vend_Amount": 9_100},

    # Abuja clusters — higher volumes
    {"Cluster": "Mogadishu Barracks",   "City": "Abuja", "Client_Type": "Military",
     "Total_Meters": 890, "Active_Meters": 845, "Online_Meters": 812,
     "Monthly_Units_Billed": 178_000, "Monthly_Units_Vended": 160_200,
     "Amount_Billed": 47_340_000, "Amount_Collected": 42_608_000,
     "Inactive_30d": 45, "Avg_Vend_Amount": 11_200},

    {"Cluster": "Mambiila Barracks",    "City": "Abuja", "Client_Type": "Military",
     "Total_Meters": 650, "Active_Meters": 612, "Online_Meters": 589,
     "Monthly_Units_Billed": 130_000, "Monthly_Units_Vended": 113_100,
     "Amount_Billed": 34_580_000, "Amount_Collected": 30_081_000,
     "Inactive_30d": 38, "Avg_Vend_Amount": 10_500},

    {"Cluster": "Niger Barracks",       "City": "Abuja", "Client_Type": "Military",
     "Total_Meters": 720, "Active_Meters": 681, "Online_Meters": 650,
     "Monthly_Units_Billed": 144_000, "Monthly_Units_Vended": 126_720,
     "Amount_Billed": 38_304_000, "Amount_Collected": 33_707_000,
     "Inactive_30d": 39, "Avg_Vend_Amount": 10_800},

    {"Cluster": "Ushafa Soldiers Camp", "City": "Abuja", "Client_Type": "Military",
     "Total_Meters": 410, "Active_Meters": 378, "Online_Meters": 361,
     "Monthly_Units_Billed": 82_000, "Monthly_Units_Vended": 70_520,
     "Amount_Billed": 21_812_000, "Amount_Collected": 18_762_000,
     "Inactive_30d": 32, "Avg_Vend_Amount": 9_800},

    {"Cluster": "D'Mayors Estate",      "City": "Abuja", "Client_Type": "Private Estate",
     "Total_Meters": 280, "Active_Meters": 251, "Online_Meters": 238,
     "Monthly_Units_Billed": 56_000, "Monthly_Units_Vended": 46_480,
     "Amount_Billed": 14_896_000, "Amount_Collected": 12_355_000,
     "Inactive_30d": 29, "Avg_Vend_Amount": 9_200},

    {"Cluster": "Defense Intelligence Agency", "City": "Abuja", "Client_Type": "Government",
     "Total_Meters": 340, "Active_Meters": 326, "Online_Meters": 318,
     "Monthly_Units_Billed": 68_000, "Monthly_Units_Vended": 61_880,
     "Amount_Billed": 18_088_000, "Amount_Collected": 16_461_000,
     "Inactive_30d": 14, "Avg_Vend_Amount": 12_400},

    {"Cluster": "Army War College",     "City": "Abuja", "Client_Type": "Military",
     "Total_Meters": 390, "Active_Meters": 368, "Online_Meters": 352,
     "Monthly_Units_Billed": 78_000, "Monthly_Units_Vended": 68_640,
     "Amount_Billed": 20_748_000, "Amount_Collected": 18_257_000,
     "Inactive_30d": 22, "Avg_Vend_Amount": 11_600},

    {"Cluster": "Nigerian Navy Barracks","City": "Abuja", "Client_Type": "Military",
     "Total_Meters": 510, "Active_Meters": 479, "Online_Meters": 458,
     "Monthly_Units_Billed": 102_000, "Monthly_Units_Vended": 89_760,
     "Amount_Billed": 27_132_000, "Amount_Collected": 23_876_000,
     "Inactive_30d": 31, "Avg_Vend_Amount": 10_900},
])

# Weekly vending pattern (transactions per day across all clusters)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
weekly_pattern = pd.DataFrame({
    "Day": days,
    "Lagos_Transactions":  [1820, 1750, 1690, 1810, 2140, 2380, 1420],
    "Abuja_Transactions":  [4250, 4180, 4090, 4310, 5020, 5480, 3210],
})

# Monthly revenue trend (8 months)
months = ["Sep'23","Oct'23","Nov'23","Dec'23","Jan'24","Feb'24","Mar'24","Apr'24"]
monthly_trend = pd.DataFrame({
    "Month": months,
    "Lagos_Revenue":  [48_200_000, 50_100_000, 51_800_000, 54_200_000,
                       53_100_000, 55_400_000, 56_800_000, 45_800_000],
    "Abuja_Revenue":  [182_400_000, 189_300_000, 195_600_000, 208_400_000,
                       204_200_000, 212_800_000, 221_500_000, 195_700_000],
})


# ─────────────────────────────────────────────
# CALCULATIONS
# ─────────────────────────────────────────────
print("\n[1/4] Processing smart meter data...")

clusters["Collection_Rate"]    = (clusters["Amount_Collected"] / clusters["Amount_Billed"] * 100).round(1)
clusters["Revenue_Leakage"]    = clusters["Amount_Billed"] - clusters["Amount_Collected"]
clusters["Vend_Rate"]          = (clusters["Monthly_Units_Vended"] / clusters["Monthly_Units_Billed"] * 100).round(1)
clusters["Connectivity_Rate"]  = (clusters["Online_Meters"] / clusters["Total_Meters"] * 100).round(1)
clusters["Inactive_Rate"]      = (clusters["Inactive_30d"] / clusters["Total_Meters"] * 100).round(1)

# Revenue Loss Risk Score (0-100, higher = more risk)
clusters["Risk_Score"] = (
    ((100 - clusters["Collection_Rate"]) * 0.40) +
    ((100 - clusters["Connectivity_Rate"]) * 0.30) +
    (clusters["Inactive_Rate"] * 2 * 0.30)
).round(1)

def risk_label(score):
    if score <= 8:  return "Low"
    elif score <= 15: return "Medium"
    else: return "High"

clusters["Risk_Label"] = clusters["Risk_Score"].apply(risk_label)

city_summary = clusters.groupby("City").agg(
    Total_Meters=("Total_Meters", "sum"),
    Online_Meters=("Online_Meters", "sum"),
    Amount_Billed=("Amount_Billed", "sum"),
    Amount_Collected=("Amount_Collected", "sum"),
    Revenue_Leakage=("Revenue_Leakage", "sum"),
    Inactive_30d=("Inactive_30d", "sum"),
).reset_index()
city_summary["Collection_Rate"] = (city_summary["Amount_Collected"] / city_summary["Amount_Billed"] * 100).round(1)
city_summary["Connectivity_Rate"] = (city_summary["Online_Meters"] / city_summary["Total_Meters"] * 100).round(1)

print(f"   Done — {len(clusters)} clusters, {clusters['Total_Meters'].sum():,} total meters")


# ─────────────────────────────────────────────
# VISUALISATIONS
# ─────────────────────────────────────────────
print("[2/4] Building dashboard...")

BLUE    = "#1f4e79"
LBLUE   = "#2e75b6"
GREEN   = "#70ad47"
ORANGE  = "#ed7d31"
RED     = "#c00000"
GOLD    = "#ffc000"
GRAY    = "#f2f2f2"

CITY_COLORS  = {"Abuja": BLUE,  "Lagos": ORANGE}
RISK_COLORS  = {"Low": GREEN, "Medium": GOLD, "High": RED}
CLIENT_COLORS= {"Military": BLUE, "Private Estate": LBLUE, "Government": GREEN}

# ── PAGE 1: Cluster Performance + Revenue Leakage + Risk Score ──
fig1, axes = plt.subplots(1, 3, figsize=(22, 8))
fig1.suptitle(
    "Smart Meter Analytics — Deharyor Global Services Ltd\n"
    "Cluster Performance, Revenue Leakage & Risk Scoring  |  Analyst: Opemipo Daniel Owolabi",
    fontsize=13, fontweight="bold", y=1.02
)

# Chart 1 — Cluster Revenue Collected (sorted)
ax1 = axes[0]
sorted_c  = clusters.sort_values("Amount_Collected", ascending=True)
bar_colors= [CITY_COLORS[c] for c in sorted_c["City"]]
bars = ax1.barh(sorted_c["Cluster"], sorted_c["Amount_Collected"] / 1e6,
                color=bar_colors, edgecolor="white")
for bar, val in zip(bars, sorted_c["Amount_Collected"]):
    ax1.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
             f"₦{val/1e6:.1f}M", va="center", fontsize=8)
ax1.set_title("Monthly Revenue Collected\nper Cluster", fontweight="bold", fontsize=11)
ax1.set_xlabel("Amount Collected (₦ Millions)")
ax1.xaxis.set_major_formatter(mticker.FormatStrFormatter("₦%.0fM"))
city_patches = [mpatches.Patch(color=CITY_COLORS[c], label=c) for c in CITY_COLORS]
ax1.legend(handles=city_patches, fontsize=9)

# Chart 2 — Revenue Leakage per cluster
ax2 = axes[1]
sorted_l  = clusters.sort_values("Revenue_Leakage", ascending=False)
leak_colors = [CITY_COLORS[c] for c in sorted_l["City"]]
bars2 = ax2.bar(range(len(sorted_l)), sorted_l["Revenue_Leakage"] / 1e6,
                color=leak_colors, edgecolor="white")
ax2.set_xticks(range(len(sorted_l)))
ax2.set_xticklabels(
    [c[:12] + ".." if len(c) > 12 else c for c in sorted_l["Cluster"]],
    rotation=40, ha="right", fontsize=8
)
for bar, val in zip(bars2, sorted_l["Revenue_Leakage"]):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
             f"₦{val/1e6:.1f}M", ha="center", fontsize=7.5, fontweight="bold")
ax2.set_title("Revenue Leakage per Cluster\n(billed but not collected)", fontweight="bold", fontsize=11)
ax2.set_ylabel("Leakage (₦ Millions)")
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("₦%.0fM"))
ax2.legend(handles=city_patches, fontsize=9)

# Chart 3 — Revenue Loss Risk Score
ax3 = axes[2]
sorted_r   = clusters.sort_values("Risk_Score", ascending=False)
risk_colors= [RISK_COLORS[r] for r in sorted_r["Risk_Label"]]
bars3 = ax3.barh(
    [c[:18] + ".." if len(c) > 18 else c for c in sorted_r["Cluster"]],
    sorted_r["Risk_Score"], color=risk_colors, edgecolor="white"
)
for bar, val, label in zip(bars3, sorted_r["Risk_Score"], sorted_r["Risk_Label"]):
    ax3.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
             f"{val}  ({label})", va="center", fontsize=8)
ax3.set_title("Revenue Loss Risk Score\n(collection + connectivity + inactivity)",
              fontweight="bold", fontsize=11)
ax3.set_xlabel("Risk Score")
ax3.invert_yaxis()
risk_patches = [mpatches.Patch(color=RISK_COLORS[r], label=r) for r in RISK_COLORS]
ax3.legend(handles=risk_patches, fontsize=9)

plt.tight_layout()
plt.savefig("/home/claude/project5/smart_meter_dashboard_page1.png", dpi=150, bbox_inches="tight")
print("   Page 1 saved")


# ── PAGE 2: Connectivity + Vending Pattern + Monthly Trend + Regional ──
fig2, axes2 = plt.subplots(2, 2, figsize=(18, 12))
fig2.suptitle(
    "Smart Meter Analytics — Connectivity Health, Vending Patterns & Regional Trends\n"
    "Deharyor Global Services Ltd  |  Analyst: Opemipo Daniel Owolabi",
    fontsize=13, fontweight="bold", y=1.01
)

# Chart 4 — Connectivity Rate per Cluster
ax4 = axes2[0, 0]
sorted_conn  = clusters.sort_values("Connectivity_Rate", ascending=True)
conn_colors  = [GREEN if v >= 90 else GOLD if v >= 80 else RED
                for v in sorted_conn["Connectivity_Rate"]]
bars4 = ax4.barh(
    [c[:18] + ".." if len(c) > 18 else c for c in sorted_conn["Cluster"]],
    sorted_conn["Connectivity_Rate"],
    color=conn_colors, edgecolor="white"
)
ax4.axvline(x=90, color=GREEN, linestyle="--", linewidth=1.5,
            alpha=0.7, label="90% Target")
for bar, val, total, online in zip(bars4,
                                    sorted_conn["Connectivity_Rate"],
                                    sorted_conn["Total_Meters"],
                                    sorted_conn["Online_Meters"]):
    ax4.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
             f"{val}%  ({online}/{total})", va="center", fontsize=8)
ax4.set_title("SIM Connectivity Rate per Cluster\n(online meters / total meters)",
              fontweight="bold", fontsize=11)
ax4.set_xlabel("Connectivity Rate (%)")
ax4.set_xlim(0, 108)
ax4.legend(fontsize=9)

# Chart 5 — Weekly Vending Pattern
ax5 = axes2[0, 1]
x     = np.arange(len(days))
width = 0.35
ax5.bar(x - width/2, weekly_pattern["Abuja_Transactions"], width,
        label="Abuja", color=BLUE, alpha=0.9, edgecolor="white")
ax5.bar(x + width/2, weekly_pattern["Lagos_Transactions"], width,
        label="Lagos", color=ORANGE, alpha=0.9, edgecolor="white")
ax5.set_xticks(x)
ax5.set_xticklabels(days, fontsize=10)
ax5.set_title("Weekly Vending Transaction Pattern\n(average transactions per day)",
              fontweight="bold", fontsize=11)
ax5.set_ylabel("Number of Transactions")
ax5.legend(fontsize=9)
ax5.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
# Annotate peak day
peak_day_abuja = weekly_pattern.loc[weekly_pattern["Abuja_Transactions"].idxmax(), "Day"]
ax5.annotate("Peak day\n(Saturday)", xy=(5, 5480), xytext=(4.2, 5200),
             fontsize=8, color=BLUE, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))

# Chart 6 — Monthly Revenue Trend
ax6 = axes2[1, 0]
ax6.plot(monthly_trend["Month"], monthly_trend["Abuja_Revenue"] / 1e6,
         marker="o", linewidth=2.5, markersize=7, color=BLUE, label="Abuja")
ax6.plot(monthly_trend["Month"], monthly_trend["Lagos_Revenue"] / 1e6,
         marker="s", linewidth=2.5, markersize=7, color=ORANGE, label="Lagos")
ax6.fill_between(monthly_trend["Month"], monthly_trend["Abuja_Revenue"] / 1e6,
                 alpha=0.08, color=BLUE)
ax6.fill_between(monthly_trend["Month"], monthly_trend["Lagos_Revenue"] / 1e6,
                 alpha=0.08, color=ORANGE)
ax6.set_title("Monthly Revenue Trend — Sep 2023 to Apr 2024\n(Abuja vs Lagos)",
              fontweight="bold", fontsize=11)
ax6.set_ylabel("Revenue (₦ Millions)")
ax6.yaxis.set_major_formatter(mticker.FormatStrFormatter("₦%.0fM"))
ax6.tick_params(axis="x", rotation=30)
ax6.legend(fontsize=9)
# Annotate Abuja dominance
ax6.annotate(f"Abuja peak:\n₦221.5M", xy=(6, 221.5), xytext=(4.5, 210),
             fontsize=8, color=BLUE, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))

# Chart 7 — Regional Summary Table
ax7 = axes2[1, 1]
ax7.axis("off")

abuja = city_summary[city_summary["City"] == "Abuja"].iloc[0]
lagos = city_summary[city_summary["City"] == "Lagos"].iloc[0]
total_meters  = clusters["Total_Meters"].sum()
total_billed  = clusters["Amount_Billed"].sum()
total_collect = clusters["Amount_Collected"].sum()
total_leakage = clusters["Revenue_Leakage"].sum()
total_inactive= clusters["Inactive_30d"].sum()

summary = f"""
PORTFOLIO SUMMARY — APRIL 2024
{'─'*42}

Total Clusters:         {len(clusters)}
Total Smart Meters:     {total_meters:,}
  of which Online:      {clusters['Online_Meters'].sum():,}  ({clusters['Online_Meters'].sum()/total_meters*100:.1f}%)
  Inactive (30d+):      {total_inactive:,} meters


REVENUE OVERVIEW
{'─'*42}

Monthly Billed:         ₦{total_billed/1e6:.1f}M
Monthly Collected:      ₦{total_collect/1e6:.1f}M
Overall Collection:     {total_collect/total_billed*100:.1f}%
Revenue Leakage:        ₦{total_leakage/1e6:.1f}M


ABUJA vs LAGOS
{'─'*42}

                  Abuja          Lagos
Clusters:         {int(abuja['Total_Meters']):>6,}        {int(lagos['Total_Meters']):>6,}  (meters)
Billed:       ₦{abuja['Amount_Billed']/1e6:>6.1f}M      ₦{lagos['Amount_Billed']/1e6:>5.1f}M
Collected:    ₦{abuja['Amount_Collected']/1e6:>6.1f}M      ₦{lagos['Amount_Collected']/1e6:>5.1f}M
Col. Rate:     {abuja['Collection_Rate']:>5.1f}%       {lagos['Collection_Rate']:>5.1f}%
Connectivity:  {abuja['Connectivity_Rate']:>5.1f}%       {lagos['Connectivity_Rate']:>5.1f}%


KEY FINDINGS
{'─'*42}

- Abuja generates {abuja['Amount_Collected']/lagos['Amount_Collected']:.1f}x more revenue than Lagos
- Saturday is peak vending day across all clusters
- DIA cluster has strongest connectivity at {clusters[clusters['Cluster']=='Defense Intelligence Agency']['Connectivity_Rate'].values[0]}%
- Ojo Barracks has highest inactive meter count
- {clusters[clusters['Risk_Label']=='High']['Cluster'].count()} cluster(s) flagged as High Risk
"""

ax7.text(0.03, 0.97, summary, transform=ax7.transAxes,
         fontsize=9, verticalalignment="top", fontfamily="monospace",
         bbox=dict(boxstyle="round", facecolor="#f0f4f8", alpha=0.85))

plt.tight_layout()
plt.savefig("/home/claude/project5/smart_meter_dashboard_page2.png", dpi=150, bbox_inches="tight")
print("   Page 2 saved")


# ─────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────
print("\n[3/4] Final business summary...")
print("\n" + "=" * 60)
print("  SMART METER PORTFOLIO — APRIL 2024")
print("=" * 60)
print(f"\n  Total Clusters:          {len(clusters)}")
print(f"  Total Smart Meters:      {total_meters:,}")
print(f"  Online Meters:           {clusters['Online_Meters'].sum():,} ({clusters['Online_Meters'].sum()/total_meters*100:.1f}%)")
print(f"  Inactive Meters (30d+):  {total_inactive:,}")
print(f"\n  Monthly Billed:          ₦{total_billed/1e6:.1f}M")
print(f"  Monthly Collected:       ₦{total_collect/1e6:.1f}M")
print(f"  Collection Rate:         {total_collect/total_billed*100:.1f}%")
print(f"  Revenue Leakage:         ₦{total_leakage/1e6:.1f}M")
print(f"\n  Abuja Revenue:           ₦{abuja['Amount_Collected']/1e6:.1f}M ({abuja['Amount_Collected']/total_collect*100:.1f}% of total)")
print(f"  Lagos Revenue:           ₦{lagos['Amount_Collected']/1e6:.1f}M ({lagos['Amount_Collected']/total_collect*100:.1f}% of total)")
print(f"\n  High Risk Clusters:      {clusters[clusters['Risk_Label']=='High']['Cluster'].tolist()}")
print(f"\n  RECOMMENDATIONS:")
print(f"  1. Investigate {total_inactive:,} inactive meters — potential revenue loss of ₦{total_inactive * clusters['Avg_Vend_Amount'].mean()/1e6:.1f}M/month")
print(f"  2. Prioritise SIM reconnection for clusters below 85% connectivity")
print(f"  3. Schedule field visits to Ojo Barracks — highest inactive meter count")
print(f"  4. Saturday vending spikes suggest end-of-week salary patterns — align field support")
print(f"\n  Analysis complete.")
print("=" * 60)
