import pandas as pd

def clean_data(df):
    report = []

    original_rows = df.shape[0]

    df = df.drop_duplicates()
    removed_duplicates = original_rows - df.shape[0]

    if removed_duplicates > 0:
        report.append(f"Removed {removed_duplicates} duplicate rows.")

    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
                report.append(f"Filled missing values in '{col}' with median.")
            else:
                mode_value = df[col].mode()
                if not mode_value.empty:
                    df[col] = df[col].fillna(mode_value[0])
                    report.append(f"Filled missing values in '{col}' with most common value.")

    for col in df.columns:
        if "date" in col.lower():
            converted = pd.to_datetime(df[col], errors="coerce")
            if converted.notna().sum() > 0:
                df[col] = converted
                report.append(f"Converted '{col}' to date format.")

    if len(report) == 0:
        report.append("No major cleaning required. Dataset looks clean.")

    return df, report