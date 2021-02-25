import pandas as pd
from tabulate import tabulate
from typing import Tuple, List


def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))

def analysis(file_name:str)->None:
    df_complete = pd.read_csv(file_name)
    df_by_dep = df.groupby("dependencia")[["Sueldo Neto"]]
    print_tabulate(df_by_dep.min().sort_values(by=["Sueldo Neto"], ascending=False))


analysis("csv/uanl.csv")
#print_tabulate(df.head(50))
