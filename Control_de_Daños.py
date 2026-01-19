import pandas as pd

def control_de_danos(df, df_name="DataFrame"):

    # NaN por columna
    missing = df.isna().sum()
    missing_pct = ((missing / len(df)) * 100).round(4)

    missing_summary = pd.DataFrame({
        'Total_values': len(df),
        'NaN_values': missing,
        'Completeness': len(df) - missing,
        'missing_pct': missing_pct
    }).sort_values('missing_pct', ascending=False)

    print("\nPorcentaje de NaN por columna:")
    print(missing_summary)


