#!/usr/bin/env python3


import requests
import io
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from typing import List, Tuple

def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def get_csv_from_url(url:str) -> pd.DataFrame:
    s=requests.get(url).content
    return pd.read_csv(io.StringIO(s.decode('utf-8')))

def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))


def limpiar_nombre_dependencia(nombre_sucio:str)->str:
    nombre_en_partes = nombre_sucio.split(' ')
    return ' '.join(nombre_en_partes[2:])

def obtener_cantidad_de_filas(df: pd.DataFrame)-> int:
    return len(df.index)

def limpiar_dato_sueldo(sueldo_txt: str)-> float:
    return float(sueldo_txt[2:].replace(",", ""))

def get_dependencias_uanl()-> Tuple[List,List[str],List[str]]:
    soup = get_soup(f"http://transparencia.uanl.mx/remuneraciones_mensuales/bxd.php")
    table = soup.find_all("table")[0].find_all('tr')
    listado_dependencias = [(option['value'], limpiar_nombre_dependencia(option.text)) for option in table[1].find_all("option")]
    listado_meses = [option['value'] for option in table[2].find_all('td')[0].find_all("option")]
    listado_anios = [option['value'] for option in table[2].find_all('td')[1].find_all("option")]
    return (listado_dependencias,listado_meses, listado_anios)

def get_pages(periodo: str, area: str)-> List[str]:
    soup = get_soup(f"http://transparencia.uanl.mx/remuneraciones_mensuales/bxd.php?pag_act=1&id_area_form={area}&mya_det={periodo}")
    try:
        links = soup.find_all("table")[1].find_all('a')
    except Exception as e:
        print(e)
        return []
    return ['1'] + [link.text for link in links]

def get_info_transparencia_uanl(periodo: str, area: str, page:int = 1) -> pd.DataFrame:
    soup = get_soup(f"http://transparencia.uanl.mx/remuneraciones_mensuales/bxd.php?pag_act={page}&id_area_form={area}&mya_det={periodo}")
    table = soup.find_all("table")
    try:
        table_row = table[2].find_all('tr')
        list_of_lists = [[row_column.text.strip() for row_column in row.find_all('td')] for row in table_row]
        df = pd.DataFrame(list_of_lists[1:], columns=list_of_lists[0])
        df["Sueldo Neto"] = df["Sueldo Neto"].transform(limpiar_dato_sueldo)
        df = df.drop(['Detalle'], axis=1)
    except Exception as e:
        print(f"pagina sin informacion a: {area}, per: {periodo}, page:{page}")
        print(e)
        df = pd.DataFrame()
    return df

def unir_datos(ldf: List[pd.DataFrame], dependencia:str, mes: str, anio:str) -> pd.DataFrame:
    if len(ldf) > 0:
        df = pd.concat(ldf)
        df["dependencia"] = [dependencia[1] for i in range(0, obtener_cantidad_de_filas(df))]
        df["mes"] = [mes for i in range(0, obtener_cantidad_de_filas(df))]
        df["anio"] = [anio for i in range(0, obtener_cantidad_de_filas(df))]
    else:
        df= pd.DataFrame()
    return df
listado_dependencias, listado_meses, listado_anios = get_dependencias_uanl()
# dependencia = listado_dependencias[1]
# mes = listado_meses[10]
# anio = listado_anios[1]
# print(f"{dependencia[1]} {mes} {anio}")
# pages = get_pages(f"{mes}{anio}", dependencia[0])
# dfs = [get_info_transparencia_uanl(f"{mes}{anio}", dependencia[0], page) for page in pages]
# df = pd.concat(dfs)
# print_tabulate(df)
# df.to_csv("uanl.csv", index=False)


#if len(dfs)> 0:
#    df = pd.concat(dfs)
#print_tabulate(df)
ldfs = []
for anio in listado_anios:
    for mes in listado_meses:
        for dependencia in listado_dependencias:
            pages = get_pages(f"{mes}{anio}", dependencia[0])
            print(f"m: {mes} a: {anio} d: {dependencia} p: {pages}")
            ldf = [get_info_transparencia_uanl(f"{mes}{anio}", dependencia[0], page) for page in pages]
            udf = unir_datos(ldf, dependencia, mes, anio)
            ldfs.append(udf)
df = pd.concat(ldfs)
df.to_csv("uanl.csv", index=False)
# df1 = get_info_transparencia_uanl(1)
# dfs = [get_info_transparencia_uanl(page) for page in range(1,10)]
# df = pd.concat(dfs)
# print(df)
# df.to_csv("uanl_ini.csv", index=False)
