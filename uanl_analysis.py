import pandas as pd
from tabulate import tabulate
from typing import Tuple, List


def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))

import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

def categorize(name:str)->str:
    if 'PREPARATORIA' in name or 'PREPA.' in name:
        return 'PREPARATORIA'
    if 'FACULTAD' in name or 'FAC.' in name:
        return 'FACULTAD'
    if 'HOSPITAL' in name:
        return 'HOSPITAL'
    if 'CENTRO' in name or 'CTRO.' in name or 'C.' in name or 'INVESTIGAC' in name :
        return 'CENTRO'
    if 'SECRETARÍA' in name or 'SECRETARIA' in name or 'SRIA.' in name or 'DIRECCIÓN' in name or 'DIRECCION' in name or \
       'DEPARTAMENTO' in name or 'DEPTO.' in name or 'CONTRALORIA' in name or 'AUDITORIA' in name or 'TESORERIA' in name \
       or 'ESCOLAR' in name or 'ABOGACÍA' in name  or 'JUNTA' in name  or 'RECTORIA' in name  or 'IMAGEN' in name :
        return 'ADMIN'
    return 'OTRO'
def normalize_data(file_name:str) -> str:
    df_complete = pd.read_csv(file_name)
    df_complete["Fecha"] = pd.to_datetime(df_complete["anio"].map(str)+ "-" + df_complete["mes"].map(str), format="%Y-%m")
    df_complete = df_complete.drop(['anio', 'mes'], axis=1)
    df_complete["Tipo"] = df_complete["dependencia"].map(categorize)
    df_complete.to_csv("csv/typed_uanl.csv", index=False)
    return "csv/typed_uanl.csv"

def analysis_dependencia(file_name:str)->None:
    df_complete = pd.read_csv(file_name)
    df_complete["Fecha"] = pd.to_datetime(df_complete["Fecha"], format="%Y-%m-%d")
    df_complete["anio"] = df_complete["Fecha"].dt.year
    df_by_dep = df_complete.groupby(["dependencia", "anio"]).agg({'Sueldo Neto': ['sum', 'count']})
    print_tabulate(df_by_dep.head())
    df_by_dep = df_complete.groupby(["dependencia", "Fecha"]).agg({'Sueldo Neto': ['sum', 'count', 'mean', 'min', 'max']})
    df_by_dep = df_by_dep.reset_index()
    print_tabulate(df_by_dep.head())


def analysis(file_name:str)->None:
    df_complete = pd.read_csv(file_name)
    # print_tabulate(df_complete[["dependencia","Tipo"]].drop_duplicates().head(150))
    df_by_dep = df_complete.groupby(["dependencia", "Fecha"])[["Sueldo Neto"]].aggregate(pd.DataFrame.sum)
    df_by_type = df_complete.groupby(["Tipo", "Fecha"])[["Sueldo Neto"]].aggregate(pd.DataFrame.sum)# .count()

    # df_by_dep_by_anio = df_by_dep.groupby(["dependencia","anio"]).aggregate(pd.DataFrame.sum).sort_values(by=["dependencia", "anio"], ascending=True)
    df_by_dep.reset_index(inplace=True)
    df_by_dep.set_index("Fecha", inplace=True)
    # print_tabulate(df_by_dep.head(5))

    # for dep in set(df_by_dep["dependencia"]):
    #    plot_by_dep(df_by_dep, dep)
    # df_aux = df_complete.groupby(["Fecha","dependencia"])[['Sueldo Neto']].mean().unstack()
    # df_aux.plot(y = 'Sueldo Neto', legend=False, figsize=(32,18))
    # plt.xticks(rotation=90)
    # plt.savefig("img/foo.png")
    # plt.close()

    df_by_type.boxplot(by = 'Tipo', figsize=(18,9))
    plt.xticks(rotation=90)
    plt.savefig("img/boxplot_tipo.png")
    plt.close()

    # aux = df_complete.groupby(["Tipo"])[["Sueldo Neto"]].aggregate(pd.DataFrame.sum)
    # aux.reset_index(inplace=True)
    df_by_type.reset_index(inplace=True)
    df_aux = df_by_type.rename(columns={"Sueldo Neto": "GastoSalarios"}).drop(['Fecha'], axis=1)
    print(df_aux.head())

    # shaphiro-wills
    # Levenes or barletts
    modl = ols("GastoSalarios ~ Tipo", data=df_aux).fit()
    anova_df = sm.stats.anova_lm(modl, typ=2)
    if anova_df["PR(>F)"][0] < 0.005:
        print("hay diferencias")
        print(anova_df)
        # Prueba tukey
        # imprimir los resultados
    else:
        print("No hay diferencias")



    # df_by_dep.boxplot(by ='dependencia', figsize=(32,18))
    # plt.xticks(rotation=90)
    # plt.savefig("img/boxplot.png")# , bbox_inches='tight')
    # plt.close()

def plot_by_dep(df: pd.DataFrame, dep:str)->None:
    df[df["dependencia"] == dep].plot(y =["Sueldo Neto"])
    plt.savefig(f"img/lt_{dep}.png")
    df[df["dependencia"] == dep].boxplot(by ='dependencia')
    plt.savefig(f"img/bplt_{dep}.png")

# normalize_data("csv/uanl.csv")
analysis("csv/typed_uanl.csv")
print("finish")
#print_tabulate(df.head(50))
