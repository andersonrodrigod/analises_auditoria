import pandas as pd

def load_excel(path="dados.xlsx"):
    return pd.read_excel(path)