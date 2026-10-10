
from pathlib import Path
import os

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "Study Habits Analysis .csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env")


def clean_data(df):
    # Remove whitespace from column names
    df.columns = df.columns.str.strip()

    # Standardize column names
    df.columns = (
        df.columns.str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )

    # Clean text columns
    for col in df.select_dtypes(include="str").columns:
        df[col] = df[col].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )

    # Convert numeric columns
    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    df["current_cgpa_or_percentage"] = pd.to_numeric(
        df["current_cgpa_or_percentage"],
        errors="coerce"
    )

    # Clean attendance percentages
    df["average_attendance_percentage"] = pd.to_numeric(
        df["average_attendance_percentage"]
        .astype("string")
        .str.replace("%", "", regex=False)
        .str.strip(),
        errors="coerce"
    )

    # Convert timestamps
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="mixed",
        errors="coerce",
        utc=True
    )

    # Correct study-day ranges converted into dates by Excel
    days_col = (
        "how_many_days_per_week_do_you_study_consistently"
    )

    df[days_col] = df[days_col].replace({
        "06-Jul": "6-7",
        "02-Mar": "2-3",
        "04-May": "4-5",
    })

    # Normalize spelling variations
    df["time_management_category"] = (
        df["how_would_you_rate_your_time_management_skills"]
        .replace({
            "Excllent": "Excellent",
            "excellent": "Excellent",
        })
    )

    # Derive study categories
    df["study_category"] = (
        df["how_many_hours_do_you_study_outside_class_daily"]
        .map({
            "Less than 1 hour": "Low",
            "1-2 hours": "Moderate",
            "2-4 hours": "High",
            "4-6 hours": "Very High",
            "More than 6 hours": "Very High",
        })
    )

    # Derive attendance categories
    df["attendance_category"] = pd.cut(
        df["average_attendance_percentage"],
        bins=[-1, 60, 75, 100],
        labels=["Low", "Moderate", "High"],
        include_lowest=True
    ).astype("string")

    # Remove completely identical rows
    df = df.drop_duplicates().copy()

    # Export cleaned data
    df.to_csv(
        OUTPUT_DIR / "cleaned_student_habits.csv",
        index=False
    )

    return df


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"CSV not found: {CSV_PATH}"
        )

    # Read CSV
    df = pd.read_csv(CSV_PATH)
    print("Original dataset:", df.shape)

    # Clean data
    df = clean_data(df)

    print("\nCleaned dataset:", df.shape)

    print("\nMissing values:")
    print(df.isnull().sum())

    # Exploratory analysis
    print("\nAverage attendance:")
    print(df["average_attendance_percentage"].mean())

    print("\nAverage recorded CGPA/percentage:")
    print(df["current_cgpa_or_percentage"].mean())

    print("\nStudy hour distribution:")
    print(
        df["how_many_hours_do_you_study_outside_class_daily"]
        .value_counts(dropna=False)
    )

    print("\nPreferred study method:")
    print(
        df["preferred_study_method"]
        .value_counts(dropna=False)
    )

    # Validate PostgreSQL configuration
    required = [
        "PG_HOST",
        "PG_PORT",
        "PG_DATABASE",
        "PG_USER",
        "PG_PASSWORD"
    ]

    missing = [
        key for key in required
        if not os.getenv(key)
    ]

    if missing:
        raise ValueError(
            f"Missing settings in .env: {', '.join(missing)}"
        )

    # Create a safe PostgreSQL connection URL
    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ["PG_USER"],
        password=os.environ["PG_PASSWORD"],
        host=os.getenv("PG_HOST", "127.0.0.1"),
        port=int(os.environ["PG_PORT"]),
        database=os.environ["PG_DATABASE"]
    )

    engine = create_engine(
        database_url,
        pool_pre_ping=True
    )

    # Load data into PostgreSQL
    # Only the clean table is replaced on each run
    try:
        with engine.begin() as connection:
            df.to_sql(
                "student_study_habits_clean",
                con=connection,
                if_exists="replace",
                index=False,
                chunksize=500
            )

            print(
                "\nData loaded into PostgreSQL successfully."
            )

            result = connection.execute(
                text(
                    "SELECT COUNT(*) "
                    "FROM student_study_habits_clean"
                )
            )

            print("Rows in PostgreSQL:", result.scalar())

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
