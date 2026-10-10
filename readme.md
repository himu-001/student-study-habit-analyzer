# Student Study Habits Analyzer

A data analytics project that explores student study habits, attendance, time management, procrastination, and academic performance using Python, PostgreSQL, SQL, and Power BI.

## Project Overview

The Student Study Habits Analyzer transforms raw student survey data into structured data for analysis and visualization. It uses Python for data cleaning and preprocessing, PostgreSQL for data storage and SQL-based analysis, and Power BI to present the results through an interactive dashboard.

The objective is to explore patterns in student study habits and understand how different habits relate to recorded academic performance.

## Tech Stack

- **Python** — data cleaning and preprocessing
- **Pandas** — data manipulation and analysis
- **PostgreSQL** — relational database and data storage
- **SQL** — querying, aggregation, and data quality checks
- **SQLAlchemy** — Python-to-PostgreSQL connectivity
- **Power BI** — interactive dashboard and visualization
- **Git & GitHub** — version control and project hosting

## Project Workflow

1. **Data Collection:** Load the student study habits survey dataset from a CSV file.
2. **Data Cleaning:** Use Python and Pandas to standardize column names, clean text values, handle data types, remove duplicate records, and create analysis categories.
3. **Data Storage:** Load the cleaned dataset into PostgreSQL.
4. **SQL Analysis:** Analyze student counts, study categories, attendance, time management, procrastination, and missing values.
5. **Visualization:** Connect Power BI to PostgreSQL and create an interactive dashboard.
6. **Insights:** Explore patterns between study habits and recorded academic scores.

## Project Structure

```text
student-study-habit-analyzer/
├── data/
│   └── Study Habits Analysis .csv
├── output/
│   └── cleaned_student_habits.csv
├── python/
│   └── analysis_pipeline.py
├── sql/
│   └── analysis_queries.sql
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

The Power BI report (`.pbix`) can also be included in the repository if its file size is reasonable.

## Dataset

The dataset contains **35 student responses** and 20 original survey columns.

The survey covers:

- Age, gender, level of study, and academic program
- Current CGPA or percentage
- Average attendance
- Daily study hours and weekly study consistency
- Exam preparation habits and preferred study methods
- Sleep duration and screen time
-