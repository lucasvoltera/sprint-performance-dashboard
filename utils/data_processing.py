import pandas as pd

def process_dataframe(df):
    if df.shape[1] < 3:
        raise ValueError("A base de dados requer uma coluna de nomes e pelo menos duas colunas de Sprints.")

    name_col = df.columns[0]
    sprint_columns = [col for col in df.columns if col != name_col]

    actual_df = df[sprint_columns].diff(axis=1)
    actual_df[sprint_columns[0]] = df[sprint_columns[0]]
    actual_df = actual_df.clip(lower=0)
    
    all_columns = actual_df.columns.tolist()
    actual_df.insert(0, name_col, df[name_col])

    return actual_df, name_col, all_columns