# Smart Meter Analytics — Energy Vending & Revenue Intelligence

**Portfolio Project 5** — IoT data analytics for smart meter infrastructure managed by **Deharyor Global Services Ltd** across military barracks and private estates in Lagos and Abuja, Nigeria.

> Built by **Opemipo Daniel Owolabi** — Senior Data Analyst | Python · SQL · Power BI · Tableau  
> Faro, Portugal | opemipoowolabi001@gmail.com

---

## Context

Deharyor Global Services Ltd installs and manages prepaid smart meters imported from Turkey, connected via SIM card (GSM/GPRS network). Each meter transmits live vending transactions and connectivity status remotely to a central data platform.

The **Nigerian Army** is the company's largest client. Abuja clusters consistently account for over 80% of total revenue.

### Cluster Areas Covered

| City | Cluster | Client Type |
|------|---------|-------------|
| Abuja | Mogadishu Barracks | Military |
| Abuja | Mambiila Barracks | Military |
| Abuja | Niger Barracks | Military |
| Abuja | Ushafa Soldiers Camp | Military |
| Abuja | Nigerian Navy Barracks | Military |
| Abuja | Army War College | Military |
| Abuja | Defense Intelligence Agency | Government |
| Abuja | D'Mayors Estate | Private Estate |
| Lagos | Ikeja Cantonment | Military |
| Lagos | Ojo Barracks | Military |
| Lagos | Pinnock Beach Estate | Private Estate |

---

## Business Problem

Smart meters generate thousands of daily transactions. Without proper analysis, management cannot answer:

1. Which clusters are generating the most revenue — and which are underperforming?
2. Where is the gap between energy billed and revenue collected?
3. Which meters have gone inactive for 30+ days — and what revenue is being lost?
4. What is the weekly vending pattern across clusters?
5. How does Abuja compare to Lagos in revenue and connectivity?
6. Which clusters have the weakest SIM connectivity — risking data loss?

---

## Dashboard Preview

![Smart Meter Dashboard Page 1](smart_meter_dashboard_page1.png)
![Smart Meter Dashboard Page 2](smart_meter_dashboard_page2.png)

---

## Key Results — April 2024

| Metric | Value |
|--------|-------|
| Total Smart Meters | 5,550 |
| Online Meters | 4,918 (88.6%) |
| Inactive Meters (30d+) | 407 |
| Monthly Billed | N277.4 Million |
| Monthly Collected | N241.9 Million |
| Collection Rate | 87.2% |
| Revenue Leakage | N35.4 Million |
| Abuja Share of Revenue | 81.1% |
| Lagos Share of Revenue | 18.9% |

---

## Six Analyses

### 1. Cluster Revenue Performance
All 11 clusters ranked by monthly revenue collected. Mogadishu Barracks tops the list at N42.6M. Abuja clusters dominate the top 8 positions, confirming the Nigerian Army as the highest-value client base.

### 2. Revenue Leakage Detection
Billed vs collected gap calculated per cluster. Total monthly leakage of N35.4M identified. Lagos clusters show proportionally higher leakage rates than Abuja — flagged for field investigation.

### 3. Revenue Loss Risk Score
Each cluster scored on three factors — collection rate (40% weight), SIM connectivity rate (30% weight), and inactive meter rate (30% weight). Ojo Barracks and Pinnock Beach Estate flagged as highest risk.

### 4. SIM Connectivity Health
Percentage of meters online per cluster. Target is 90%. Defense Intelligence Agency leads at 93.5%. Clusters below 85% are flagged for SIM maintenance — offline meters mean lost transaction data and lost revenue.

### 5. Weekly Vending Pattern
Saturday is consistently the peak vending day across all clusters in both cities — likely aligned with end-of-week salary payments. This insight allows field support teams to be deployed more effectively.

### 6. Monthly Revenue Trend
8-month trend (Sep 2023 to Apr 2024) showing Abuja generating 4.3x more revenue than Lagos. Abuja peaked at N221.5M in March 2024. The April dip across both cities warrants further investigation.

---

## How to Run

```bash
git clone https://github.com/opemipo-analytics/smart-meter-analytics.git
cd smart-meter-analytics

pip install pandas numpy matplotlib seaborn

python smart_meter_analytics.py
```

---

## Tools and Technologies

| Tool | Purpose |
|------|---------|
| Python 3 | Core scripting and pipeline |
| Pandas | Data aggregation and transformation |
| Matplotlib | Multi-panel dashboard visualisations |
| NumPy | Numerical calculations |

---

## Skills Demonstrated

- IoT data analytics — processing smart meter transaction and connectivity data
- Revenue intelligence — leakage detection, inactive meter identification, risk scoring
- Composite risk scoring — multi-factor weighted scoring model
- Operational analytics — translating meter data into field action recommendations
- Regional comparison — city-level performance benchmarking

---

## Other Projects

| Project | Description |
|---------|-------------|
| [AEDC Marketer Performance](https://github.com/opemipo-analytics/AEDC-MARKETERS-ANALYTICS) | Python analysis of electricity marketer KPIs |
| [AEDC Revenue Forecasting ML](https://github.com/opemipo-analytics/aedc-revenue-forecasting) | Machine Learning revenue forecast — 99.8% accuracy |
| [AEDC Customer Segmentation](https://github.com/opemipo-analytics/aedc-customer-segmentation) | SQL and RFM customer segmentation |
| [AMCON Portfolio Analytics](https://github.com/opemipo-analytics/amcon-portfolio-analytics) | Financial property portfolio analysis |

---

*Built from real operational experience as a Senior Data Analyst at Deharyor Global Services Ltd, managing smart meter infrastructure across military and civilian clusters in Nigeria.*
