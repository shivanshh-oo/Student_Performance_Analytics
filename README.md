# Student Performance & Attendance Analytics

ML pipeline to flag at-risk students early in the semester using attendance and performance data. Built during a 6-week Data Science internship (May–Jul 2026) — uses synthetic data since the original institutional dataset is confidential.

## How to run

```bash
pip install -r requirements.txt
cd scripts && python generate_data.py && cd ..
jupyter notebook notebooks/student_performance_attendance_analytics.ipynb
```

## Structure

```
├── notebooks/   → main analysis notebook
├── scripts/     → synthetic data generation
├── data/        → generated dataset
├── models/      → exported model (.pkl)
├── PRD.md       → product requirements doc
```

## Tech stack

Python, Pandas, NumPy, Scikit-learn, XGBoost, Matplotlib, Seaborn
