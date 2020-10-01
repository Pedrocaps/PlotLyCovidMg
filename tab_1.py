import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
import dash
import plotly.express as px


class FirstTab:
    def __init__(self, df: pd.DataFrame, app: dash.Dash):
        self.df = df
        self.app = app

    def get_tab(self) -> html.Div:
        div = html.Div([
            html.H1("Serviços", style={'text-align': 'center', 'float': 'center'}),
            self.filter_service_tab(4)
        ],

            style={"border": "2px yellow dashed", 'width': '30%'})

        return div

    def get_tab_2(self) -> html.Div:
        df = self.df[['codigo_servico','descricao_servico']]
        df = df.groupby(['descricao_servico'])[['codigo_servico']].count().sort_values('codigo_servico', ascending=False)
        df = df.reset_index()

        df = df.head(20)

        bar_plt = px.bar(
            df,
            x=df['descricao_servico'],
            y=df['codigo_servico']
        )

        slider = dcc.Slider(
            id='slider-updatemode',
            min=0,
            max=40,
            step=5,
            value=10,
            tooltip={
                'always_visible': True,
                'placement': 'bottomRight'
            }
        )

        div = html.Div([
            html.H1("Top", style={'text-align': 'center'}),
            slider,
            dcc.Graph(id='top_10', figure=bar_plt)

        ],
            style={"border": "2px black solid"})

        return div

    def filter_service_tab(self, max_col) -> html.Div:
        service_list = self.df.sort_values('codigo_servico', ascending=True)['codigo_servico'].unique()
        service_list = service_list.tolist()

        service_list = np.array_split(service_list, max_col)

        options_html_list = []

        for i in range(max_col):
            options_html_list.append(
                html.Div(
                    style={'width': '20%', 'height': '100%', 'float': 'left', "border": "2px black solid"},
                    children=[
                        dcc.Checklist(className=f'checkbox_{i}',
                                      options=[{'label': str(i), 'value': i} for i in service_list[i]],
                                      labelStyle={'display': 'block'},
                                      ),
                    ]
                )
            )

        services_div = html.Div(options_html_list,
                                style={'width': '100%'})

        return services_div
