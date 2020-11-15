import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import first_tab
from data_obj import EnumType
from data_obj import SingletonDadosCoord
from data_obj import SingletonDadosCovid

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

DATA = 'DATA'
MUNICIPIO = 'MUNICIPIO_RESIDENCIA'
NUM_CASOS = 'NUM_CASOS'
CODIGO_IBGE = 'CodigoIBGE'
URS = 'URS'
MICRO = 'Micro'
MACRO = 'Macro'
LAT = 'LATITUDE'
LON = 'LONGITUDE'

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)

colors = {
    'background': '#252e3f',
    'text': '#7fafdf'
}

df_class = SingletonDadosCovid(EnumType.CONFIRMADOS)


def second_div() -> html.Div:
    df_base = df_class.get_dados_covid()
    df2 = df_base.groupby([MUNICIPIO])[[NUM_CASOS]].sum().sort_values(NUM_CASOS, ascending=False)
    df2 = df2.head(10)
    df2.reset_index(inplace=True)

    bar_plt = px.bar(
        df2,
        x=df2[MUNICIPIO],
        y=df2[NUM_CASOS]
    )

    div = html.Div([
        html.H1("Top 10", style={'text-align': 'center'}),
        dcc.Graph(id='top_10', figure=bar_plt)

    ],
        style={"border": "2px black solid"})

    return div


def third_graph() -> html.Div:
    df_base = df_class.get_dados_covid()
    dff = df_base.copy().sort_values(NUM_CASOS, ascending=False)
    top_10 = dff[MUNICIPIO].unique()[:10]
    dff = dff[dff[MUNICIPIO].isin(top_10)]

    dff = dff.sort_values([MUNICIPIO, DATA], ascending=True)

    lines_plt = px.line(
        data_frame=dff,
        x=DATA,
        y=NUM_CASOS,
        color=MUNICIPIO,
        orientation='v',
        labels={
            NUM_CASOS: 'Numero de Casos',
            DATA: 'Mes'
        }
    )

    div = html.Div([
        html.H1("Top 10 progressão", style={'text-align': 'center'}),

        dcc.Graph(id='top_10_line', figure=lines_plt)

    ],
        style={"border": "2px black solid"})

    return div


# ------------------------------------------------------------------------------
# App layout
second = second_div()
third = third_graph()


def get_app_layout():
    return \
        html.Div(
            id='root',
            children=[
                dcc.Tabs(
                    id="tabs-with-classes",
                    value='tab-1',
                    parent_className='custom-tabs',
                    className='custom-tabs-container',
                    children=[
                        dcc.Tab(
                            label='Perfil Geográfico MG',
                            value='tab-1',
                            className='custom-tab',
                            selected_className='custom-tab--selected'
                        ),
                        # dcc.Tab(
                        #     label='Tab two',
                        #     value='tab-2',
                        #     className='custom-tab',
                        #     selected_className='custom-tab--selected'
                        # ),
                        # dcc.Tab(
                        #     label='Tab three, multiline',
                        #     value='tab-3', className='custom-tab',
                        #     selected_className='custom-tab--selected'
                        # ),
                    ]
                ),

                html.Div(id='tabs-content-classes')
            ],
        )


app.layout = get_app_layout()


@app.callback(Output('tabs-content-classes', 'children'),
              [Input('tabs-with-classes', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return first_tab.first_tab()
    elif tab == 'tab-2':
        return second
    elif tab == 'tab-3':
        return third


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='my_bee_map', component_property='figure'),
     Output(component_id='drpd_mun', component_property='options'),
     Output(component_id='drpd_urs', component_property='options'),
     Output(component_id='drpd_micro', component_property='options'),
     Output(component_id='drpd_macro', component_property='options')],
    [Input(component_id='drpd_mun', component_property='value'),
     Input(component_id='drpd_urs', component_property='value'),
     Input(component_id='drpd_micro', component_property='value'),
     Input(component_id='drpd_macro', component_property='value')]

)
def update_graph(slctd_mun, slctd_urs, slctd_micro, slctd_macro):
    df_base = df_class.get_dados_covid()
    df_graph = df_base.copy().drop(['CodigoIBGE'], axis=1).sort_values(DATA, ascending=True)

    df_graph['DATA'] = pd.to_datetime(df_graph[DATA], dayfirst=True).dt.month
    distinct_months = sorted(df_graph[DATA].unique().tolist())

    list_mun = df_graph[MUNICIPIO].unique().tolist()
    list_urs = df_graph[URS].unique().tolist()
    list_micro = df_graph[MICRO].unique().tolist()
    list_macro = df_graph[MACRO].unique().tolist()

    if slctd_mun:
        df_graph = df_graph[df_graph[MUNICIPIO] == slctd_mun]
        list_urs = df_graph[URS][~df_graph[URS].isna()].unique().tolist()
        list_micro = df_graph[MICRO].unique().tolist()
        list_macro = df_graph[MACRO].unique().tolist()

        df_graph = df_graph.groupby([MUNICIPIO, DATA])[[NUM_CASOS]].sum()
        df_graph = df_graph.groupby(MUNICIPIO).cumsum()
    elif slctd_urs:
        df_graph = df_graph[df_graph[URS] == slctd_urs]
        list_mun = df_graph[MUNICIPIO].unique().tolist()
        list_micro = df_graph[MICRO].unique().tolist()
        list_macro = df_graph[MACRO].unique().tolist()

        df_graph = df_graph.groupby([URS, DATA])[[NUM_CASOS]].sum()
        df_graph = df_graph.groupby(URS).cumsum()
    elif slctd_micro:
        df_graph = df_graph[df_graph[MICRO] == slctd_micro]
        list_urs = df_graph[URS][~df_graph[URS].isna()].unique().tolist()
        list_mun = df_graph[MUNICIPIO].unique().tolist()
        list_macro = df_graph[MACRO].unique().tolist()

        df_graph = df_graph.groupby([MICRO, DATA])[[NUM_CASOS]].sum()
        df_graph = df_graph.groupby(MICRO).cumsum()
    elif slctd_macro:
        df_graph = df_graph[df_graph[MACRO] == slctd_macro]
        list_urs = df_graph[URS][~df_graph[URS].isna()].unique().tolist()
        list_mun = df_graph[MUNICIPIO].unique().tolist()
        list_micro = df_graph[MICRO].unique().tolist()

        df_graph = df_graph.groupby([MACRO, DATA])[[NUM_CASOS]].sum()
        df_graph = df_graph.groupby(MACRO).cumsum()
    else:
        df_graph = df_graph.groupby([DATA])[[NUM_CASOS]].sum()
        df_graph = df_graph.groupby(DATA).cumsum()

    list_dict_mun = [{"label": mun, "value": mun} for mun in sorted(list_mun)]
    list_dict_urs = [{"label": mun, "value": mun} for mun in sorted(list_urs)]
    list_dict_micro = [{"label": mun, "value": mun} for mun in sorted(list_micro)]
    list_dict_macro = [{"label": mun, "value": mun} for mun in sorted(list_macro)]

    df_graph.reset_index(inplace=True)

    fig1 = go.Figure(go.Scatter(
        x=df_graph[DATA],
        y=df_graph[NUM_CASOS],
        orientation='v',
        hovertemplate='Qtd. Casos: %{y}<extra></extra>'
    ))

    fig1.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=distinct_months,
            title='Mës'
        ),
        yaxis=dict(
            title='Quantidade'
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            color=colors['text']
        )
    )

    return fig1, list_dict_mun, list_dict_urs, list_dict_micro, list_dict_macro


@app.callback(
    Output(component_id='top_10', component_property='figure'),
    [Input(component_id='slider_top', component_property='value')]
)
def update_top_num(slide_slct):
    df_base = df_class.get_dados_covid()
    df2 = df_base.copy()

    df2 = df2.groupby([MUNICIPIO])[[NUM_CASOS]].sum().sort_values(NUM_CASOS, ascending=False)

    df2 = df2[slide_slct[0] - 1: slide_slct[1]]
    df2.reset_index(inplace=True)

    df2 = df2.sort_values(NUM_CASOS, ascending=True)

    x = df2[NUM_CASOS]
    y = df2[MUNICIPIO]

    fig1 = go.Figure(go.Bar(
        x=x,
        y=y,
        orientation='h'
    ))

    fig1.update_layout(
        xaxis=dict(
            title='Municipio'
        ),
        yaxis=dict(
            title='Quantidade'
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            color=colors['text']
        )
    )

    return fig1


@app.callback(
    Output(component_id='top_progress', component_property='figure'),
    [Input(component_id='slider_top', component_property='value')]
)
def update_progress(slide_slct):
    df_base = df_class.get_dados_covid()
    dff = df_base.copy().sort_values(NUM_CASOS, ascending=False)[[MUNICIPIO, DATA, NUM_CASOS]]
    dff[DATA] = pd.to_datetime(dff[DATA], dayfirst=True)

    top_10 = dff[MUNICIPIO].unique()[:10]
    dff = dff[dff[MUNICIPIO].isin(top_10)]

    dff = dff.sort_values(MUNICIPIO, ascending=True)

    dff = dff.groupby([MUNICIPIO, DATA])[[NUM_CASOS]].sum()
    dff = dff.groupby(level=[0]).cumsum()

    dff.reset_index(inplace=True)

    lines_plt = px.line(
        data_frame=dff,
        x=DATA,
        y=NUM_CASOS,
        color=MUNICIPIO,
        orientation='v',
        labels={
            NUM_CASOS: 'Numero de Casos',
            DATA: 'Mes'
        }
    )

    lines_plt.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            color=colors['text']
        )
    )

    return lines_plt


@app.callback(
    Output(component_id='out_titulo', component_property='children'),
    Input(component_id='drpd_tipo_geo', component_property='value')
)
def update_data(drop_data):
    if drop_data == 'confirmado':
        ret = 'Casos Confirmados'
        df_class.change_data_source(EnumType.CONFIRMADOS)
    elif drop_data == 'obito':
        ret = 'Obitos'
        df_class.change_data_source(EnumType.CONFIRMADOS)
    elif drop_data == 'recuperado':
        ret = 'Casos Recuperados'
        df_class.change_data_source(EnumType.CONFIRMADOS)
    elif drop_data == 'internado':
        ret = 'Pessoas Internadas'
        df_class.change_data_source(EnumType.CONFIRMADOS)
    else:
        ret = 'Painel'

    return f'Painel {ret}'


@app.callback(
    Output(component_id='dist_geo', component_property='figure'),
    Input(component_id='drpd_tipo_geo', component_property='value')
)
def update_geo(drop_data):
    coord = SingletonDadosCoord().get_dados()
    dff = df_class.get_dados_covid()

    dff = dff.groupby([CODIGO_IBGE])[[NUM_CASOS]].sum().sort_values(NUM_CASOS, ascending=False)

    dff.reset_index(inplace=True)
    dff = pd.merge(dff, coord, on=CODIGO_IBGE)

    center_lat = dff[LAT].mean()
    center_lon = dff[LON].mean()
    max = dff[NUM_CASOS].max() / 2
    min = dff[NUM_CASOS].min()

    fig = px.density_mapbox(dff, lat=LAT, lon=LON, z=NUM_CASOS, radius=30,
                            center=dict(lat=center_lat, lon=center_lon), zoom=5,
                            mapbox_style="stamen-terrain",
                            range_color=[min, max],
                            hover_name='NOME_MUNICIPIO',
                            hover_data={NUM_CASOS: True, LAT: False, LON: False})

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            color=colors['text']
        )
    )
    fig.update(layout_coloraxis_showscale=False)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
