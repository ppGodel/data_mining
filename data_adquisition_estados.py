import requests
import io
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from typing import Tuple, List
import re
from datetime import datetime

def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def get_csv_from_url(url:str) -> pd.DataFrame:
    s=requests.get(url).content
    return pd.read_csv(io.StringIO(s.decode('utf-8')))

def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))



def wiki() -> pd.DataFrame:
    soup = get_soup("https://en.wikipedia.org/wiki/List_of_states_of_Mexico")
    list_of_lists = [] # :List
    rows = soup.table.find_all('tr')
    for row in rows[1:]:
        columns = row.find_all('td')
        #  listado_de_valores_en_columnas = []
        #  for column in columns:
        #    listado_de_valores_en_columnas.append(coulmn.text.strip())
        listado_de_valores_en_columnas = [column.text.strip() for column in columns]
        list_of_lists.append(listado_de_valores_en_columnas)

    return pd.DataFrame(list_of_lists, columns=[header.text.strip() for header in  rows[0].find_all('th')])


df = wiki()
print_tabulate(df)
df.to_csv("csv/estados.csv", index=False)

def remove_repeated_number(str_repeated_value:str)->float:
    if(type(str_repeated_value)!=str):
        str_repeated_value = str(str_repeated_value)
    str_sin_0 = re.sub("^0+", '', str_repeated_value)
    str_sin_comma = str_sin_0.replace(',','')
    num = 0.0
    if len(str_sin_comma) % 2 == 0:
        mitad = int(len(str_sin_comma)/2)
        num = float(str_sin_comma[0:mitad])
    return num

def remove_repeated_date(str_date_repeated:str) -> datetime:
    return datetime.strptime(str_date_repeated[0:8],'%Y%m%d')

def limpiar_area(area:str)->Tuple[float,float]:
    str_en_partes = re.findall(r'[\d,\.]*', area)
    str_en_partes.remove('2')
    blancos = str_en_partes.count('')
    for blanco in range(0, blancos):
        str_en_partes.remove('')

    km_str = str_en_partes[0]
    km_float = remove_repeated_number(km_str)
    mi_str = str_en_partes[1]
    mi_float = float(mi_str.replace(',',''))
    return (km_float, mi_float)

df = pd.read_csv("csv/estados.csv")
df = df.drop(['Coat of arms'], axis=1)
# print(df.columns)
df.columns = ['estado',
       'nombre_oficial',
       'capital', 'ciudad_mas_grande', 'area', 'poblacion_2020',
       'num_de_municipios', 'lugar',
       'fecha_de_admision']
# print(df.columns)
df['lugar'] = df['lugar'].transform(remove_repeated_number)
df['poblacion_2020'] = df['poblacion_2020'].transform(remove_repeated_number)
df['fecha_de_admision'] = df['fecha_de_admision'].transform(remove_repeated_date)
areas= df['area'].transform(limpiar_area).to_list()
df['area_km2'] =[a[0] for a in areas]
df['area_mi'] =[a[1] for a in areas]
df = df.drop(['area'], axis=1)
print_tabulate(df)
df.to_csv("csv/estados_limpio.csv", index=False)
