import pandas as pd
from tabulate import tabulate
from typing import Tuple, List


def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))

def analysis(file_name:str)->pd.DataFrame:
    df = pd.read_csv(file_name)
    return df
print_tabulate(analysis("csv/uanl.csv"))
