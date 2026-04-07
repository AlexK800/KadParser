import pandas as pd

def read_cases(path: str) -> list[str]:
    df = pd.read_excel(path)
    return df["case_number"].astype(str).tolist()
