import dash_core_components as dcc
import dash_html_components as html


def first_tab() -> html.Div:
    return html.Div(
        id='tab_1_container',
        children=[
            html.Div(
                children=[
                    html.H1("Painel", style={'text-align': 'center'}),
                    html.Div(
                        className="outer_div",
                        children=[
                            html.Div(
                                className='container one-half column',
                                children=div_num_casos()
                            ),
                            html.Div(
                                className='container one-half column',
                                children=div_top_num_casos()
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                children=div_top_progressao()
            )
        ]
    )


def div_top_num_casos() -> list:
    return [
        html.Div(
            className='grid_first_graph',
            children=[
                html.H1("Top Num. de Casos", style={'text-align': 'center'}, className='graph_title'),

                html.Div(
                    className="grid_filter_1st_graph",
                    children=[
                        html.Div(
                            className="filter_local",
                            children=[
                                html.P('Slides from x to y', style={'text-align': 'center'}),
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
            className='grid_first_graph',
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
