import pandas as pd
from tabulate import tabulate
from typing import Tuple, List


def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))

def analysis(file_name:str)->None:
    df_complete = pd.read_csv(file_name)
    df_complete["Fecha"] = pd.to_datetime(df_complete["anio"].map(str)+ "-" + df_complete["mes"].map(str), format="%Y-%m")
    df_complete = df_complete.drop(['anio', 'mes'], axis=1)
    df_by_dep = df_complete.groupby(["dependencia", "Fecha"])[["Sueldo Neto"]].aggregate(sum)
    # df_by_dep_by_anio = df_by_dep.groupby(["dependencia","anio"]).aggregate(pd.DataFrame.sum).sort_values(by=["dependencia", "anio"], ascending=True)
    df_by_dep.reset_index(inplace=True)
    df_by_dep.set_index("Fecha", inplace=True)
    print_tabulate(df_by_dep.head())

    # for dep in set(df_by_dep["dependencia"]):
    #     plot_by_dep(df_by_dep, dep)
    # df_by_dep.groupby("dependencia")["Sueldo Neto"].plot(y = ["Sueldo Neto"])
    # plt.savefig("img/foo.png")# , bbox_inches='tight')

    df_by_dep.boxplot(by ='dependencia')
    plt.savefig("img/boxplot.png")# , bbox_inches='tight')

def plot_by_dep(df: pd.DataFrame, dep:str)->None:
    df[df["dependencia"] == dep].plot(y =["Sueldo Neto"])
    plt.savefig(f"img/lt_{dep}.png")
    df[df["dependencia"] == dep].boxplot(by ='dependencia')
    plt.savefig(f"img/bplt_{dep}.png")

analysis("csv/uanl.csv")
#print_tabulate(df.head(50))
