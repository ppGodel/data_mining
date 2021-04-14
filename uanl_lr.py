import pandas as pd
from tabulate import tabulate
from typing import Tuple, List


def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns.tolist(), tablefmt='orgtbl'))

import matplotlib.pyplot as plt
import statsmodels.api as sm
import numbers


def transform_variable(df: pd.DataFrame, x:str)->pd.Series:
    if isinstance(df[x][0], numbers.Number):
        return df[x] # type: pd.Series
    else:
        return pd.Series([i for i in range(0, len(df[x]))])


def linear_regression(df: pd.DataFrame, x:str, y: str)->None:
    fixed_x = transform_variable(df, x)
    model= sm.OLS(df[y],sm.add_constant(fixed_x)).fit()
    print(model.summary())

    coef = pd.read_html(model.summary().tables[1].as_html(),header=0,index_col=0)[0]['coef']
    df.plot(x=x,y=y, kind='scatter')
    plt.plot(df[x],[pd.DataFrame.mean(df[y]) for _ in fixed_x.items()], color='green')
    plt.plot(df_by_sal[x],[ coef.values[1] * x + coef.values[0] for _, x in fixed_x.items()], color='red')
    plt.xticks(rotation=90)
    plt.savefig(f'img/lr_{y}_{x}.png')
    plt.close()


df = pd.read_csv("csv/typed_uanl.csv") # type: pd.DataFrame
#print_tabulate(df.head(50))
df_by_sal = df.groupby("Fecha")\
              .aggregate(sueldo_mensual=pd.NamedAgg(column="Sueldo Neto", aggfunc=pd.DataFrame.mean))
# df_by_sal["sueldo_mensual"] = df_by_sal["sueldo_mensual"]**10
print_tabulate(df_by_sal.head(5))
linear_regression(df_by_sal, "Fecha", "sueldo_mensual")
