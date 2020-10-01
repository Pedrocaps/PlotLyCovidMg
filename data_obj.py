import pandas as pd


class DataObj():
    def __init__(self, path, delimiter):
        self.path = path
        self.delimiter = delimiter
        self.df = self.get_df()

    def get_df(self) -> pd.DataFrame:
        return pd.read_csv(self.path, delimiter=self.delimiter, encoding='utf-8')
