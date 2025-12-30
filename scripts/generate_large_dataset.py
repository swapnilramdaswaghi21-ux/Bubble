import pandas as pd
import numpy as np

np.random.seed(42)

industries = {
    "AI": ["NVIDIA", "Palantir", "AMD", "Snowflake", "C3AI"],
    "EV": ["Tesla", "BYD", "Rivian", "Lucid", "Nio"],
    "Infra": ["AdaniPorts", "LarsenToubro", "Vinci", "ACS", "Ferrovial"],
    "Internet": ["Zomato", "DoorDash", "Uber", "Meituan", "Grab"],
    "FinTech": ["Paytm", "Block", "Adyen", "SoFi", "Stripe"],
    "Pharma": ["Pfizer", "Moderna", "Biogen", "Gilead", "SunPharma"],
    "RealEstate": ["DLF", "Lennar", "Evergrande", "BrookfieldRE"],
    "Energy": ["Exxon", "Chevron", "BP", "Shell", "ONGC"]
}

years = range(2014, 2025)
rows = []

for industry, firms in industries.items():
    for firm in firms:
        base_em = np.random.uniform(0.8, 1.6)
        base_peg = np.random.uniform(1.2, 2.8)
        base_de = np.random.uniform(0.3, 2.0)

        for year in years:
            cycle = (year - 2014) / 10
            em = base_em + np.random.normal(0, 0.25) + cycle
            peg = base_peg + np.random.normal(0, 0.5) + cycle * 1.2
            fscore = max(2, 9 - em - np.random.uniform(0, 2))
            de = base_de + np.random.normal(0, 0.4) + cycle
            cfo = np.random.normal(0.08 - cycle * 0.1, 0.08)

            crash_prob = (0.3*em + 0.3*peg + 0.3*de - 0.3*cfo) / 6
            crash = np.random.rand() < crash_prob

            ret = np.random.uniform(-0.65, -0.25) if crash else np.random.uniform(-0.05, 0.35)

            rows.append([
                firm, industry, year,
                round(em,2), round(peg,2), int(fscore),
                round(de,2), round(cfo,2), round(ret,2)
            ])

df = pd.DataFrame(rows, columns=[
    "Firm","Industry","Year","Hybrid_EM","PEG","F_Score",
    "Debt_Equity","CFO_Growth","Return"
])

df.to_csv("data/large_panel_dataset.csv", index=False)
print("Large dataset created:", len(df), "rows")
