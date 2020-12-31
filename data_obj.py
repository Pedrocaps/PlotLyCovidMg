import pathlib
import os
from enum import Enum

import pandas as pd


class EnumType(Enum):
    path = os.path.dirname(__file__)
    CONFIRMADOS = os.path.join(path, 'dados', 'covid_mg_31_12.csv') # f"{path}\\dados\\covid_mg_31_12.csv"
    OBITOS = "covid_mg_obitos.csv"
    RECUPERADOS = "covid_mg_recuperados.csv"
    INTERNADOS = "covid_mg_internados.csv"


def get_enum_by_name(drop_data) -> EnumType:
    if drop_data == 'confirmado':
        return EnumType.CONFIRMADOS
    elif drop_data == 'obito':
        return EnumType.OBITOS
    elif drop_data == 'recuperado':
        return EnumType.RECUPERADOS
    elif drop_data == 'internado':
        return EnumType.INTERNADOS


class SingletonDadosCovid:
    def __init__(self, enum_type, delimiter=';'):
        self.df = None
        self.enum_type = enum_type
        self.path = enum_type.value
        self.delimiter = delimiter
        self.default_path = ""

    def get_dados_covid(self) -> pd.DataFrame:
        df_base = pd.read_csv(self.path, delimiter=self.delimiter, encoding='utf-8',
                              dtype={'CodigoIBGE': str})
        self.default_path = self.path
        self.df = df_base
        return self.df.dropna(axis=0)

    def change_data_source(self, enum_type):
        if enum_type == self.enum_type:
            return
        else:
            self.path = enum_type.value
            self.df = None


class SingletonDadosCoord:
    def __init__(self):
        self.df = None
        self.path = 'coord_municipios.csv'
        self.delimiter = ';'

    def get_dados(self):
        if self.df is None:
            df_base = pd.read_csv(self.path, delimiter=self.delimiter, encoding='utf-8')

            df_base['CodigoIBGE'] = df_base['CodigoIBGE'].map(lambda x: str(x)[:-1])
            df_base['LATITUDE'] = df_base['LATITUDE'].map(lambda x: str(x.replace(',', '.'))).astype('float')
            df_base['LONGITUDE'] = df_base['LONGITUDE'].map(lambda x: str(x.replace(',', '.'))).astype('float')

            # drop nan values from dataframe
            return df_base.dropna(axis=0)
        else:
            return self.df


def get_all_files_covid() -> list:
    lista_arq = []
    for p in pathlib.Path('dados').iterdir():
        if p.is_file():
            lista_arq.append(p)

    lista_arq = [{"label": f"{str(arq).split('_')[2]}/{str(arq).split('_')[3][:2]}",
                  "value": str(arq)} for arq in sorted(lista_arq, reverse=True)]

    return lista_arq


def get_dados_from_list(todos_mun):
    df_list = []
    for arq in todos_mun:
        df_base = pd.read_csv(arq, delimiter=';', encoding='utf-8',
                              dtype={'CodigoIBGE': str})
        df_list.append(df_base.dropna(axis=0))

    return df_list
