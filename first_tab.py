import dash_core_components as dcc
import dash_html_components as html
from data_obj import get_all_files_covid

def first_tab() -> html.Div:
    return html.Div(
        id='tab_1_container',
        children=[
            html.Div(
                children=div_titulo()
            ),
            html.Div(
                children=[
                    html.Div(
                        className="outer_div",
                        children=[
                            html.Div(
                                className='container one-third column',
                                children=div_num_casos()
                            ),
                            html.Div(
                                className='container one-third column',
                                children=div_top_num_casos()
                            ),
                            html.Div(
                                className='container one-third column',
                                children=div_progress_bar()
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                children=[
                    html.Div(
                        className="outer_div",
                        children=[
                            html.Div(
                                className='container one-half column',
                                children=div_top_progressao()
                            ),
                            html.Div(
                                className='container one-half column',
                                children=div_mapa()
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                children=[
                    html.Div(
                        className="outer_div",
                        children=[
                            html.Div(
                                className='container',
                                children=div_por_data()
                            )
                        ]
                    )
                ]
            )
        ]
    )


def div_por_data():
    return [
        html.Div(
            children=[
                html.H1("Número de Casos por Data", style={'text-align': 'center'}, className='graph_title'),

                html.Div(
                    className="grid_filter_graph",
                    children=[
                        html.Div(
                            className="filter_local",
                            children=[
                                html.P('Data do Arquivo'),
                                dcc.Dropdown(id="drpd_data",
                                             options=get_all_files_covid(),
                                             multi=True,
                                             placeholder="Mais Atual",
                                             )]),
                    ]),

                dcc.Graph(id='grafico_por_data_arquivo', figure={})
            ]
        )
    ]


def div_progress_bar() -> list:
    return [
        html.Div(
            children=[
                html.H1("Progressão / Total Mensal", style={'text-align': 'center'}, className='graph_title'),
                html.P('Escolha Municípios para remover do gráfico', style={'text-align': 'center'}),
                html.Div(
                    children=[dcc.Dropdown(
                        id="todos_mun",
                        options=[],
                        multi=True
                    )]
                ),
                html.Br(),

                dcc.Graph(id='progess_tot_bar', figure={})
            ]
        )
    ]


def div_mapa() -> list:
    return [
        html.H1("Distribuição", style={'text-align': 'center'}),
        html.Div(
            children=[
                dcc.Graph(id='dist_geo', figure={})
            ]
        )
    ]


def div_titulo() -> list:
    return [
        html.H1(id="out_titulo", style={'text-align': 'center'}),

        dcc.Dropdown(id="drpd_tipo_geo",
                     options=[
                         {'label': 'Confirmados', 'value': 'confirmado'},
                         # {'label': 'Obitos', 'value': 'obito'},
                         # {'label': 'Recuperados', 'value': 'recuperado'},
                         # {'label': 'Internados', 'value': 'internado'}
                     ],
                     multi=False,
                     value="confirmado"
                     )
    ]


def div_top_num_casos() -> list:
    return [
        html.Div(
            children=[
                html.H1("Top Num. de Casos", style={'text-align': 'center'}, className='graph_title'),

                html.Div(
                    className="grid_filter_1st_graph",
                    children=[
                        html.Div(
                            className="filter_local",
                            children=[
                                html.P('Arraste para top x a top y', style={'text-align': 'center'}),
                                dcc.RangeSlider(
                                    id='slider_top',
                                    min=1,
                                    max=20,
                                    step=1,
                                    marks={
                                        i: str(i) for i in range(1, 20, 2)
                                    },
                                    value=[1, 10]
                                )
                            ])
                    ]),

                dcc.Graph(id='top_10', figure={})
            ]
        )
    ]


def div_num_casos() -> list:
    return [
        html.Div(
            children=[
                html.H1("Número de Casos", style={'text-align': 'center'}, className='graph_title'),

                html.Div(
                    className="grid_filter_graph",
                    children=[
                        html.Div(
                            className="filter_local",
                            children=[
                                html.P('Municipio'),
                                dcc.Dropdown(id="drpd_mun",
                                             options=[],
                                             multi=False,
                                             placeholder="Todos"
                                             )]),
                        html.Div(
                            className="filter_local",
                            children=[
                                html.P('URS'),
                                dcc.Dropdown(id="drpd_urs",
                                             options=[],
                                             multi=False,
                                             placeholder="Todos"
                                             )]),
                        html.Div(
                            className="filter_local",
                            children=[
                                html.P('Micro Reg.'),
                                dcc.Dropdown(id="drpd_micro",
                                             options=[],
                                             multi=False,
                                             placeholder="Todos"
                                             )]),
                        html.Div(
                            className="filter_local",
                            children=[
                                html.P('Macro Reg.'),
                                dcc.Dropdown(id="drpd_macro",
                                             options=[],
                                             multi=False,
                                             placeholder="Todos"
                                             )])
                    ]),

                dcc.Graph(id='my_bee_map', figure={})
            ]
        )
    ]


def div_top_progressao() -> list:
    return [
        html.H1("Top 10 progressão", style={'text-align': 'center'}),
        html.Div(
            children=[
                dcc.Graph(id='top_progress', figure={})
            ]
        )
    ]
