"""Synthetic demo trial for the promo film (not real patients). Usage: python make_demo_data.py"""
import csv
import numpy as np
from pathlib import Path

rng = np.random.default_rng(2026)
n = 240
here = Path(__file__).parent
group = np.where(np.arange(n) % 2 == 0, 'Treatment', 'Control')
rng.shuffle(group)
trt = (group == 'Treatment').astype(float)
age = np.clip(rng.normal(58, 10, n), 30, 85).round(0)
sex = np.where(rng.random(n) < 0.47, 'Female', 'Male')
bmi = np.clip(rng.normal(25.5, 3.6, n), 17, 40).round(1)
smoking = rng.choice(['Never', 'Former', 'Current'], n, p=[0.5, 0.3, 0.2])
diabetes = (rng.random(n) < 0.28).astype(int)
sbp_base = np.clip(rng.normal(146, 12, n), 115, 190).round(0)
sbp_12w = np.clip(sbp_base - 6 - 9.5 * trt + rng.normal(0, 11, n), 100, 190).round(0)
ldl = np.clip(rng.normal(3.4, 0.8, n) - 0.45 * trt, 1.2, 6.5).round(2)
crp = np.exp(rng.normal(1.0, 0.6, n) - 0.35 * trt + 0.02 * (bmi - 25)).round(2)
biomarker = np.clip(rng.normal(5.0, 1.3, n) + 0.04 * (age - 58), 1, 10).round(2)
lin = -0.6 * trt + 0.035 * (age - 58) + 0.5 * (biomarker - 5) + 0.35 * diabetes + 0.25 * (ldl - 3.4)
haz = 0.018 * np.exp(lin)
t_event = rng.exponential(1 / haz)
t_cens = rng.uniform(18, 60, n)
time = np.minimum(t_event, t_cens).round(1)
event = (t_event <= t_cens).astype(int)
qol = np.clip(70 + 6 * trt - 0.25 * (sbp_12w - 135) - 3 * diabetes + rng.normal(0, 8, n), 20, 100).round(0)
for arr, rate in ((bmi, 0.04), (ldl, 0.05), (crp, 0.03)):
    arr[rng.random(n) < rate] = np.nan

cols = dict(patient_id=[f'P{i + 1:04d}' for i in range(n)], group=group, age=age.astype(int), sex=sex, bmi=bmi,
            smoking=smoking, diabetes=diabetes, sbp_baseline=sbp_base.astype(int), sbp_12w=sbp_12w.astype(int), ldl=ldl,
            crp=crp, biomarker=biomarker, time_months=time, event=event, qol_score=qol.astype(int))
with open(here / 'demo_trial.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(cols)
    for i in range(n):
        w.writerow(['' if isinstance(v[i], float) and np.isnan(v[i]) else v[i] for v in cols.values()])

studies = [('Chen 2019', -0.42, 0.18), ('Garcia 2020', -0.15, 0.22), ('Okafor 2020', -0.51, 0.30), ('Larsen 2021', -0.22, 0.14),
           ('Tanaka 2021', -0.60, 0.35), ('Muller 2022', 0.05, 0.25), ('Singh 2023', -0.38, 0.16), ('Rossi 2024', -0.29, 0.20)]
with open(here / 'demo_meta.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['study', 'effect', 'se'])
    w.writerows(studies)
print('events', event.sum(), 'sbp diff', sbp_12w[trt == 1].mean() - sbp_12w[trt == 0].mean())
