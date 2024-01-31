import pandas as pd
from tabulate import tabulate
from typing import Tuple, List


def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))

import matplotlib.pyplot as plt
# import statsmodels.api as sm
# from statsmodels.formula.api import ols

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

def transform_into_typed_df(raw_df: pd.DataFrame)->pd.DataFrame:
    raw_df["Fecha"] = pd.to_datetime(raw_df["anio"].map(str)+ "-" + raw_df["mes"].map(str), format="%Y-%m")
    raw_df = raw_df.drop(['anio', 'mes'], axis=1)
    raw_df["Tipo"] = raw_df["dependencia"].map(categorize)
    return raw_df



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
    # df_by_dep = df_complete.groupby(["dependencia", "anio"]).agg({'Sueldo Neto': ['sum', 'count']})
    # print_tabulate(df_by_dep.head())
    df_by_dep = df_complete.groupby(["dependencia", "Fecha"]).agg({'Sueldo Neto': ['sum', 'count', 'mean', 'min', 'max']})
    df_by_dep = df_by_dep.reset_index()
    print_tabulate(df_by_dep.head())
    df_by_dep.to_csv("csv/uanl_dependencia_mes.csv")


def create_boxplot_by_type(file_name:str, column: str, agg_fn= pd.DataFrame.sum):
    df_complete = pd.read_csv(file_name)
    df_by_type = df_complete.groupby([column,"Fecha"])[["Sueldo Neto"]].aggregate(agg_fn)# .count()
    df_by_type.boxplot(by = column, figsize=(27,18))
    plt.xticks(rotation=90)
    plt.savefig(f"img/boxplot_{column}.png")
    plt.close()


def plot_by_dep(df: pd.DataFrame, dep:str)->None:
    df[df["dependencia"] == dep].plot(y =["Sueldo Neto"])
    plt.savefig(f"img/lt_{dep}.png")
    df[df["dependencia"] == dep].boxplot(by ='dependencia')
    plt.savefig(f"img/bplt_{dep}.png")


def create_plot_por_dependencia(file_name:str):
    df_complete = pd.read_csv(file_name)
    df_by_dep = df_complete.groupby(["dependencia", "Fecha"])[["Sueldo Neto"]].aggregate(pd.DataFrame.mean)
    df_by_dep.reset_index(inplace=True)
    df_by_dep.set_index("Fecha", inplace=True)

    for dep in set(df_by_dep["dependencia"]):
       plot_by_dep(df_by_dep, dep)
    df_aux = df_complete.groupby(["Fecha","dependencia"])[['Sueldo Neto']].mean().unstack()
    df_aux.plot(y = 'Sueldo Neto', legend=False, figsize=(32,18))
    plt.xticks(rotation=90)
    plt.savefig("img/foo.png")
    plt.close()

def anova(df_aux: pd.DataFrame, str_ols: str):
    # shaphiro-wills
    # Levenes or barletts
    modl = ols(str_ols, data=df_aux).fit()
    anova_df = sm.stats.anova_lm(modl, typ=2)
    if anova_df["PR(>F)"][0] < 0.005:
        print("hay diferencias")
        print(anova_df)
        # Prueba tukey
        # imprimir los resultados
    else:
        print("No hay diferencias")

def anova_1(file_name: str):
    df_complete = pd.read_csv(file_name)
    df_by_type = df_complete.groupby(["Tipo", "Fecha"])[["Sueldo Neto"]].aggregate(pd.DataFrame.sum)
    df_by_type.reset_index(inplace=True)
    df_by_type.set_index("Fecha", inplace=True)
    df_by_type.reset_index(inplace=True)
    df_aux = df_by_type.rename(columns={"Sueldo Neto": "GastoSalarios"}).drop(['Fecha'], axis=1)
    print(df_aux.head())
    anova(df_aux, "GastoSalarios ~ Tipo")

def analysis(file_name:str)->None:
    df_complete = pd.read_csv(file_name)
    # print_tabulate(df_complete[["dependencia","Tipo"]].drop_duplicates().head(150))
    df_by_dep = df_complete.groupby(["dependencia", "Fecha"])[["Sueldo Neto"]].aggregate(pd.DataFrame.sum)

    # df_by_dep_by_anio = df_by_dep.groupby(["dependencia","anio"]).aggregate(pd.DataFrame.sum).sort_values(by=["dependencia", "anio"], ascending=True)
    df_by_dep.reset_index(inplace=True)
    df_by_dep.set_index("Fecha", inplace=True)
    # print_tabulate(df_by_dep.head(5))

    for dep in set(df_by_dep["dependencia"]):
       plot_by_dep(df_by_dep, dep)
    # df_aux = df_complete.groupby(["Fecha","dependencia"])[['Sueldo Neto']].mean().unstack()
    # df_aux.plot(y = 'Sueldo Neto', legend=False, figsize=(32,18))
    # plt.xticks(rotation=90)
    # plt.savefig("img/foo.png")
    # plt.close()

    df_by_type = df_complete.groupby(["Tipo", "Fecha"])[["Sueldo Neto"]].aggregate(pd.DataFrame.sum)# .count()
    df_by_type.boxplot(by = 'Tipo', figsize=(18,9))
    plt.xticks(rotation=90)
    plt.savefig("img/boxplot_tipo.png")
    plt.close()

    # aux = df_complete.groupby(["Tipo"])[["Sueldo Neto"]].aggregate(pd.DataFrame.sum)
    # aux.reset_index(inplace=True)
    # df_by_type.reset_index(inplace=True)
    # df_aux = df_by_type.rename(columns={"Sueldo Neto": "GastoSalarios"}).drop(['Fecha'], axis=1)
    # print(df_aux.head())

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



def create_typed_df(filename:str)-> pd.DataFrame:
    df_complete = pd.read_csv(filename)
    raw_df = transform_into_typed_df(df_complete)
    print_tabulate(raw_df.head(50))
    raw_df.to_csv("csv/typed_uanl.csv", index=False)
    return raw_df

def show_type_of_department():
    df_complete = pd.read_csv("csv/typed_uanl.csv")
    print_tabulate(df_complete[["dependencia","Tipo"]].\
                   drop_duplicates().head(150))

def show_data_by_dependency_and_date():
    df_complete = pd.read_csv("csv/typed_uanl.csv")
    df_by_dep = df_complete.groupby(["dependencia", "Fecha"])[["Sueldo Neto"]].aggregate(pd.DataFrame.sum)
    df_by_dep.reset_index(inplace=True)
    df_by_dep.set_index("Fecha", inplace=True)
    print_tabulate(df_by_dep[df_by_dep["dependencia"]== "FAC. DE CIENCIAS FISICO-MATEMATICAS"].head(50))


def show_data_by_type_and_date():
    df_complete = pd.read_csv("csv/typed_uanl.csv")
    df_by_type = df_complete.groupby(["Tipo", "Fecha"])[["Sueldo Neto"]].aggregate(pd.DataFrame.sum)
    df_by_type.reset_index(inplace=True)
    df_by_type.set_index("Fecha", inplace=True)
    print_tabulate(df_by_type.head(150))


def show_salary_and_count_by_type_and_date():
    df_complete = pd.read_csv("csv/typed_uanl.csv")
    df_by_type = df_complete.groupby(["Tipo", "Fecha"]).agg({'Sueldo Neto': ['sum', 'count', 'mean', 'min']})
    df_by_type.reset_index(inplace=True)
    df_by_type.columns = ['Tipo', 'Fecha', 'Total_sueldos', 'Conteo_Empleado', 'Promedio_sueldo', 'Salario_Maximo']
    df_by_type.set_index("Fecha", inplace=True)
    print_tabulate(df_by_type.head(150))

def show_salary_and_count_by_dependency_and_date():
    df_complete = pd.read_csv("csv/typed_uanl.csv")
    df_by_type = df_complete.groupby(["dependencia", "Fecha"]).agg({'Sueldo Neto': ['sum', 'count', 'mean', 'max']})
    df_by_type.reset_index(inplace=True)
    df_by_type.columns = ['Tipo', 'Fecha', 'Total_sueldos', 'Conteo_Empleado', 'Promedio_sueldo', 'Salario_Maximo']
    df_by_type.set_index("Fecha", inplace=True)
    print_tabulate(df_by_type)


if __name__ == "__main__":
    # analysis_dependencia("csv/typed_uanl.csv")
    # create_typed_df("csv/uanl.csv")
    # show_data_by_dependency_and_date()
    # show_data_by_type_and_date()
    # show_salary_and_count_by_type_and_date()
    # show_salary_and_count_by_dependency_and_date()
    analysis("csv/uanl.csv")
    # create_boxplot_by_type("csv/typed_uanl.csv", 'dependencia', pd.DataFrame.mean)#"Tipo")
    # create_plot_por_dependencia("csv/typed_uanl.csv")
    # anova_1("csv/typed_uanl.csv")
