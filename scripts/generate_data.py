import pandas as pd
import numpy as np
import os

np.random.seed(42)
N = 1500

departments = ['Computer Science', 'Mechanical', 'Civil', 'Electronics', 'Information Technology']
semesters = list(range(1, 9))
admission_years = [2022, 2023, 2024, 2025]

student_ids = [f"STU{str(i).zfill(4)}" for i in range(1, N + 1)]
depts = np.random.choice(departments, N)
sems = np.random.choice(semesters, N)
years = np.random.choice(admission_years, N)

attendance = np.clip(np.random.normal(78, 15, N), 5, 100)
cgpa = np.clip(3.0 + (attendance / 100) * 6.0 + np.random.normal(0, 1.0, N), 0, 10)

backlogs = []
for c, a in zip(cgpa, attendance):
    if c > 8 and a > 85:
        p = [0.85, 0.1, 0.05, 0, 0, 0]
    elif c > 6 and a > 70:
        p = [0.55, 0.2, 0.15, 0.1, 0, 0]
    elif c > 4.5 and a > 50:
        p = [0.15, 0.25, 0.25, 0.2, 0.1, 0.05]
    else:
        p = [0.0, 0.1, 0.15, 0.3, 0.25, 0.2]
    backlogs.append(np.random.choice(range(6), p=p))

trends = []
for b in backlogs:
    if b == 0:
        trends.append(np.random.choice(['Improving', 'Stable', 'Declining'], p=[0.5, 0.4, 0.1]))
    elif b <= 2:
        trends.append(np.random.choice(['Improving', 'Stable', 'Declining'], p=[0.2, 0.45, 0.35]))
    else:
        trends.append(np.random.choice(['Improving', 'Stable', 'Declining'], p=[0.05, 0.2, 0.75]))

study_hours = np.clip(attendance / 10 + np.random.normal(0, 2, N), 0, 16)

data = pd.DataFrame({
    'Student_ID': student_ids,
    'Department': depts,
    'Semester': sems,
    'Admission_Year': years,
    'Attendance_Pct': np.round(attendance, 1),
    'CGPA': np.round(cgpa, 2),
    'Num_Backlogs': backlogs,
    'Marks_Trend': trends,
    'Study_Hours_Per_Day': np.round(study_hours, 1),
})

# --- inject real-world messiness ---

# 1. duplicate rows (~3%)
dup_idx = np.random.choice(N, size=45, replace=False)
data = pd.concat([data, data.iloc[dup_idx]], ignore_index=True)

# 2. missing values scattered across columns
for col, frac in [('Attendance_Pct', 0.04), ('CGPA', 0.03), ('Num_Backlogs', 0.02),
                   ('Study_Hours_Per_Day', 0.05), ('Marks_Trend', 0.02)]:
    mask = np.random.random(len(data)) < frac
    data.loc[mask, col] = np.nan

# 3. typos / inconsistent department names
typo_map = {
    'Computer Science': ['Comp Science', 'computer science', 'CS', 'Computer Sci'],
    'Mechanical': ['mechanical', 'Mech', 'MECHANICAL'],
    'Electronics': ['electronics', 'ECE', 'Elec'],
    'Information Technology': ['IT', 'Info Tech', 'information technology'],
    'Civil': ['civil', 'CIVIL']
}
for i in range(len(data)):
    if np.random.random() < 0.08:
        dept = data.at[i, 'Department']
        if dept in typo_map:
            data.at[i, 'Department'] = np.random.choice(typo_map[dept])

# 4. some attendance values above 100 (data entry errors)
err_idx = np.random.choice(len(data), size=12, replace=False)
data.loc[err_idx, 'Attendance_Pct'] = np.random.uniform(101, 115, size=12).round(1)

# 5. negative CGPA (clearly wrong entries)
bad_cgpa = np.random.choice(len(data), size=8, replace=False)
data.loc[bad_cgpa, 'CGPA'] = np.random.uniform(-2, -0.1, size=8).round(2)

# 6. semester as string in some rows
str_idx = np.random.choice(len(data), size=30, replace=False)
data['Semester'] = data['Semester'].astype(object)
for i in str_idx:
    data.at[i, 'Semester'] = str(data.at[i, 'Semester'])

# 7. whitespace in some Student_IDs
ws_idx = np.random.choice(len(data), size=20, replace=False)
for i in ws_idx:
    data.at[i, 'Student_ID'] = ' ' + data.at[i, 'Student_ID'] + ' '

# shuffle rows
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

os.makedirs('../data', exist_ok=True)
data.to_csv('../data/synthetic_student_data.csv', index=False)
print(f"Generated {len(data)} records (with intentional noise) -> data/synthetic_student_data.csv")
