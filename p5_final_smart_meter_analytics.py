"""
Smart Meter Analytics — Energy Vending, Revenue Loss and Connectivity
=====================================================================
Author: Opemipo Daniel Owolabi
Project: Portfolio Project 5 — IoT Data Analytics and Revenue Intelligence
Tools: Python, Pandas, Matplotlib

Note:
-----
All company names, client names, cluster locations and identifying
information have been anonymised to protect client confidentiality.
Clusters are referred to as Cluster A through Cluster K. Regions are
referred to as Region 1 and Region 2. The analytical approach,
methodology and findings reflect real work conducted during
professional employment in the smart meter infrastructure sector.

Business Problem:
-----------------
A smart meter infrastructure company installed and managed prepaid
smart meters connected via SIM card (GSM/GPRS) across multiple
clusters in two regions. Management needed visibility into:

  1. Which clusters generate the most revenue
  2. Where the gap between billing and collection exists
  3. Which meters have gone inactive for 30 or more days
  4. What the weekly vending pattern looks like
  5. How the two regions compare in revenue performance
  6. Which clusters have the weakest SIM connectivity
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
print("  SMART METER ANALYTICS")
print("  ENERGY VENDING AND REVENUE INTELLIGENCE")
print("  Analyst: Opemipo Daniel Owolabi")
print("=" * 60)


# ── DATA ──
clusters = pd.DataFrame([
    # Region 1
    {"Cluster":"Cluster A","Region":"Region 1","Client_Type":"Private Estate",
     "Total_Meters":320,"Active_Meters":285,"Online_Meters":271,
     "Amount_Billed":12_850_000,"Amount_Collected":10_920_000,"Inactive_30d":35},
    {"Cluster":"Cluster B","Region":"Region 1","Client_Type":"Government",
     "Total_Meters":480,"Active_Meters":420,"Online_Meters":398,
     "Amount_Billed":19_200_000,"Amount_Collected":15_840_000,"Inactive_30d":60},
    {"Cluster":"Cluster C","Region":"Region 1","Client_Type":"Government",
     "Total_Meters":560,"Active_Meters":498,"Online_Meters":471,
     "Amount_Billed":22_400_000,"Amount_Collected":19_040_000,"Inactive_30d":62},
    # Region 2
    {"Cluster":"Cluster D","Region":"Region 2","Client_Type":"Government",
     "Total_Meters":890,"Active_Meters":845,"Online_Meters":812,
     "Amount_Billed":47_340_000,"Amount_Collected":42_608_000,"Inactive_30d":45},
    {"Cluster":"Cluster E","Region":"Region 2","Client_Type":"Government",
     "Total_Meters":650,"Active_Meters":612,"Online_Meters":589,
     "Amount_Billed":34_580_000,"Amount_Collected":30_081_000,"Inactive_30d":38},
    {"Cluster":"Cluster F","Region":"Region 2","Client_Type":"Government",
     "Total_Meters":720,"Active_Meters":681,"Online_Meters":650,
     "Amount_Billed":38_304_000,"Amount_Collected":33_707_000,"Inactive_30d":39},
    {"Cluster":"Cluster G","Region":"Region 2","Client_Type":"Government",
     "Total_Meters":410,"Active_Meters":378,"Online_Meters":361,
     "Amount_Billed":21_812_000,"Amount_Collected":18_762_000,"Inactive_30d":32},
    {"Cluster":"Cluster H","Region":"Region 2","Client_Type":"Private Estate",
     "Total_Meters":280,"Active_Meters":251,"Online_Meters":238,
     "Amount_Billed":14_896_000,"Amount_Collected":12_355_000,"Inactive_30d":29},
    {"Cluster":"Cluster I","Region":"Region 2","Client_Type":"Government",
     "Total_Meters":340,"Active_Meters":326,"Online_Meters":318,
     "Amount_Billed":18_088_000,"Amount_Collected":16_461_000,"Inactive_30d":14},
    {"Cluster":"Cluster J","Region":"Region 2","Client_Type":"Government",
     "Total_Meters":390,"Active_Meters":368,"Online_Meters":352,
     "Amount_Billed":20_748_000,"Amount_Collected":18_257_000,"Inactive_30d":22},
    {"Cluster":"Cluster K","Region":"Region 2","Client_Type":"Government",
     "Total_Meters":510,"Active_Meters":479,"Online_Meters":458,
     "Amount_Billed":27_132_000,"Amount_Collected":23_876_000,"Inactive_30d":31},
])

days    = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
weekly  = pd.DataFrame({
    "Day":   days,
    "Day_Order": range(1,8),
    "Region1_Transactions": [1820,1750,1690,1810,2140,2380,1420],
    "Region2_Transactions": [4250,4180,4090,4310,5020,5480,3210],
})

months  = ["Sep-23","Oct-23","Nov-23","Dec-23","Jan-24","Feb-24","Mar-24","Apr-24"]
trend   = pd.DataFrame({
    "Month":            months,
    "Region1_Revenue":  [48.2,50.1,51.8,54.2,53.1,55.4,56.8,45.8],
    "Region2_Revenue":  [182.4,189.3,195.6,208.4,204.2,212.8,221.5,195.7],
})


# ── CALCULATIONS ──
clusters["Collection_Rate"]   = (clusters["Amount_Collected"] / clusters["Amount_Billed"] * 100).round(1)
clusters["Revenue_Leakage"]   = clusters["Amount_Billed"] - clusters["Amount_Collected"]
clusters["Connectivity_Rate"] = (clusters["Online_Meters"]  / clusters["Total_Meters"]   * 100).round(1)
clusters["Inactive_Rate"]     = (clusters["Inactive_30d"]   / clusters["Total_Meters"]   * 100).round(1)
clusters["Offline_Meters"]    = clusters["Total_Meters"] - clusters["Online_Meters"]
clusters["Risk_Score"]        = (
    ((100 - clusters["Collection_Rate"]) * 0.40) +
    ((100 - clusters["Connectivity_Rate"]) * 0.30) +
    (clusters["Inactive_Rate"] * 2 * 0.30)
).round(1)
clusters["Risk_Label"] = clusters["Risk_Score"].apply(
    lambda x: "High" if x > 15 else ("Medium" if x > 8 else "Low")
)

reg_sum = clusters.groupby("Region").agg(
    Total_Meters=("Total_Meters","sum"),
    Online_Meters=("Online_Meters","sum"),
    Amount_Billed=("Amount_Billed","sum"),
    Amount_Collected=("Amount_Collected","sum"),
    Revenue_Leakage=("Revenue_Leakage","sum"),
    Inactive_30d=("Inactive_30d","sum"),
).reset_index()

total_meters  = clusters["Total_Meters"].sum()
total_billed  = clusters["Amount_Billed"].sum()
total_collect = clusters["Amount_Collected"].sum()
total_leakage = clusters["Revenue_Leakage"].sum()
total_inactive= clusters["Inactive_30d"].sum()

print(f"\n   {len(clusters)} clusters | {total_meters:,} total meters")


# ── COLOURS ──
BLUE  = "#1f4e79"; ORANGE="#ed7d31"; GREEN="#70ad47"
RED   = "#c00000"; GOLD  ="#ffc000"
RCOLS = {"Region 2":BLUE,"Region 1":ORANGE}
RISK  = {"Low":GREEN,"Medium":GOLD,"High":RED}


# ── PAGE 1 — Cluster performance, leakage, risk ──
fig1, axes = plt.subplots(1, 3, figsize=(22, 8))
fig1.suptitle(
    "Smart Meter Analytics — Cluster Performance, Revenue Leakage and Risk Scoring\n"
    "Analyst: Opemipo Daniel Owolabi",
    fontsize=13, fontweight="bold", y=1.02
)

ax1 = axes[0]
sc  = clusters.sort_values("Amount_Collected", ascending=True)
ax1.barh(sc["Cluster"], sc["Amount_Collected"]/1e6,
         color=[RCOLS.get(r,"#999") for r in sc["Region"]], edgecolor="white")
for i, (_, row) in enumerate(sc.iterrows()):
    ax1.text(row["Amount_Collected"]/1e6+0.2, i,
             f"N{row['Amount_Collected']/1e6:.1f}M", va="center", fontsize=8)
ax1.set_title("Monthly Revenue Collected per Cluster", fontweight="bold", fontsize=11)
ax1.set_xlabel("Amount Collected (N Millions)")
ax1.xaxis.set_major_formatter(mticker.FormatStrFormatter("N%.0fM"))
ax1.legend(handles=[mpatches.Patch(color=c,label=l) for l,c in RCOLS.items()], fontsize=9)

ax2 = axes[1]
sl  = clusters.sort_values("Revenue_Leakage", ascending=False)
ax2.bar(range(len(sl)), sl["Revenue_Leakage"]/1e6,
        color=[RCOLS.get(r,"#999") for r in sl["Region"]], edgecolor="white")
ax2.set_xticks(range(len(sl)))
ax2.set_xticklabels(sl["Cluster"], rotation=40, ha="right", fontsize=8)
for i, (_, row) in enumerate(sl.iterrows()):
    ax2.text(i, row["Revenue_Leakage"]/1e6+0.05,
             f"N{row['Revenue_Leakage']/1e6:.1f}M", ha="center", fontsize=7.5, fontweight="bold")
ax2.set_title("Revenue Leakage per Cluster\n(billed but not collected)", fontweight="bold", fontsize=11)
ax2.set_ylabel("Leakage (N Millions)")
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("N%.0fM"))
ax2.legend(handles=[mpatches.Patch(color=c,label=l) for l,c in RCOLS.items()], fontsize=9)

ax3 = axes[2]
sr  = clusters.sort_values("Risk_Score", ascending=False)
ax3.barh(sr["Cluster"], sr["Risk_Score"],
         color=[RISK[r] for r in sr["Risk_Label"]], edgecolor="white")
for i, (_, row) in enumerate(sr.iterrows()):
    ax3.text(row["Risk_Score"]+0.2, i,
             f"{row['Risk_Score']}  ({row['Risk_Label']})", va="center", fontsize=8)
ax3.set_title("Revenue Loss Risk Score per Cluster", fontweight="bold", fontsize=11)
ax3.set_xlabel("Risk Score")
ax3.invert_yaxis()
ax3.legend(handles=[mpatches.Patch(color=c,label=l) for l,c in RISK.items()], fontsize=9)

plt.tight_layout()
plt.savefig("/home/claude/clean/project5/smart_meter_dashboard_page1.png", dpi=150, bbox_inches="tight")
plt.close()


# ── PAGE 2 — Connectivity, vending pattern, trend, summary ──
fig2, axes2 = plt.subplots(2, 2, figsize=(18, 12))
fig2.suptitle(
    "Smart Meter Analytics — Connectivity Health, Vending Patterns and Regional Trends\n"
    "Analyst: Opemipo Daniel Owolabi",
    fontsize=13, fontweight="bold", y=1.01
)

ax4 = axes2[0, 0]
sc2 = clusters.sort_values("Connectivity_Rate", ascending=True)
ax4.barh(sc2["Cluster"], sc2["Connectivity_Rate"],
         color=[GREEN if v>=90 else GOLD if v>=80 else RED for v in sc2["Connectivity_Rate"]],
         edgecolor="white")
ax4.axvline(x=90, color=GREEN, linestyle="--", linewidth=1.5, alpha=0.7, label="90% Target")
for i, (_, row) in enumerate(sc2.iterrows()):
    ax4.text(row["Connectivity_Rate"]+0.2, i,
             f"{row['Connectivity_Rate']}%  ({row['Online_Meters']}/{row['Total_Meters']})",
             va="center", fontsize=8)
ax4.set_title("SIM Connectivity Rate per Cluster\n(online / total meters)", fontweight="bold", fontsize=11)
ax4.set_xlabel("Connectivity Rate (%)")
ax4.set_xlim(0, 108)
ax4.legend(fontsize=9)

ax5 = axes2[0, 1]
x = np.arange(len(days)); w = 0.35
ax5.bar(x-w/2, weekly["Region2_Transactions"], w, label="Region 2", color=BLUE,   alpha=0.9, edgecolor="white")
ax5.bar(x+w/2, weekly["Region1_Transactions"], w, label="Region 1", color=ORANGE, alpha=0.9, edgecolor="white")
ax5.set_xticks(x)
ax5.set_xticklabels(days, fontsize=10)
ax5.set_title("Weekly Vending Transaction Pattern\n(average transactions per day)", fontweight="bold", fontsize=11)
ax5.set_ylabel("Number of Transactions")
ax5.legend(fontsize=9)
ax5.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{int(x):,}"))

ax6 = axes2[1, 0]
ax6.plot(trend["Month"], trend["Region2_Revenue"], marker="o", linewidth=2.5, markersize=7, color=BLUE,   label="Region 2")
ax6.plot(trend["Month"], trend["Region1_Revenue"], marker="s", linewidth=2.5, markersize=7, color=ORANGE, label="Region 1")
ax6.fill_between(trend["Month"], trend["Region2_Revenue"], alpha=0.08, color=BLUE)
ax6.fill_between(trend["Month"], trend["Region1_Revenue"], alpha=0.08, color=ORANGE)
ax6.set_title("Monthly Revenue Trend — Sep 2023 to Apr 2024", fontweight="bold", fontsize=11)
ax6.set_ylabel("Revenue (N Millions)")
ax6.yaxis.set_major_formatter(mticker.FormatStrFormatter("N%.0fM"))
ax6.tick_params(axis="x", rotation=30)
ax6.legend(fontsize=9)

ax7 = axes2[1, 1]
ax7.axis("off")
r2 = reg_sum[reg_sum["Region"]=="Region 2"].iloc[0]
r1 = reg_sum[reg_sum["Region"]=="Region 1"].iloc[0]
summary = f"""
PORTFOLIO SUMMARY — APRIL 2024
{'─'*38}

Total Clusters:      {len(clusters)}
Total Smart Meters:  {total_meters:,}
  Online:            {clusters['Online_Meters'].sum():,}  ({clusters['Online_Meters'].sum()/total_meters*100:.1f}%)
  Inactive (30d+):   {total_inactive:,} meters


REVENUE OVERVIEW
{'─'*38}

Monthly Billed:      N{total_billed/1e6:.1f}M
Monthly Collected:   N{total_collect/1e6:.1f}M
Collection Rate:     {total_collect/total_billed*100:.1f}%
Revenue Leakage:     N{total_leakage/1e6:.1f}M


REGION 2 vs REGION 1
{'─'*38}

                Region 2    Region 1
Billed:     N{r2['Amount_Billed']/1e6:>6.1f}M  N{r1['Amount_Billed']/1e6:>5.1f}M
Collected:  N{r2['Amount_Collected']/1e6:>6.1f}M  N{r1['Amount_Collected']/1e6:>5.1f}M
Col. Rate:   {r2['Amount_Collected']/r2['Amount_Billed']*100:>5.1f}%    {r1['Amount_Collected']/r1['Amount_Billed']*100:>5.1f}%


KEY FINDINGS
{'─'*38}

- Region 2 generates {r2['Amount_Collected']/r1['Amount_Collected']:.1f}x more revenue
- Saturday is peak vending day
- {clusters[clusters['Risk_Label']=='High']['Cluster'].count()} cluster(s) flagged as High Risk
- {total_inactive:,} inactive meters require investigation
"""
ax7.text(0.03, 0.97, summary, transform=ax7.transAxes,
         fontsize=9, verticalalignment="top", fontfamily="monospace",
         bbox=dict(boxstyle="round", facecolor="#f0f4f8", alpha=0.85))

plt.tight_layout()
plt.savefig("/home/claude/clean/project5/smart_meter_dashboard_page2.png", dpi=150, bbox_inches="tight")
plt.close()


# ── SUMMARY ──
print(f"\n  Total Smart Meters:   {total_meters:,}")
print(f"  Monthly Billed:       N{total_billed/1e6:.1f}M")
print(f"  Monthly Collected:    N{total_collect/1e6:.1f}M")
print(f"  Collection Rate:      {total_collect/total_billed*100:.1f}%")
print(f"  Revenue Leakage:      N{total_leakage/1e6:.1f}M")
print(f"  Region 2 Share:       {r2['Amount_Collected']/total_collect*100:.1f}%")
print(f"  Region 1 Share:       {r1['Amount_Collected']/total_collect*100:.1f}%")
print(f"  High Risk Clusters:   {clusters[clusters['Risk_Label']=='High']['Cluster'].tolist()}")
print("\n  Dashboards saved.")
print("=" * 60)
