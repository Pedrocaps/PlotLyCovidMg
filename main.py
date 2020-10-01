import pandas as pd
import numpy as np
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import first_tab

app = dash.Dash(__name__, suppress_callback_exceptions=True)

DATA = 'DATA'
MUNICIPIO = 'MUNICIPIO_RESIDENCIA'
NUM_CASOS = 'NUM_CASOS'
CODIGO_IBGE = 'CodigoIBGE'
URS = 'URS'
MICRO = 'Micro'
MACRO = 'Macro'


def get_df() -> pd.DataFrame:
    return pd.read_csv("covid_mg.csv", delimiter=';')


# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df_base = get_df()
# drop nan values from dataframe
df_base = df_base.dropna(axis=0)

df = df_base.copy()

df = df.drop(['CodigoIBGE', 'URS', 'Micro', 'Macro'], axis=1)
df['DATA'] = pd.to_datetime(df[DATA], dayfirst=True)

df = df.groupby([MUNICIPIO, DATA])[[NUM_CASOS]].sum()
df = df.groupby(MUNICIPIO).cumsum()
df.reset_index(inplace=True)

df = df[df[DATA] < '2020-08-01']

colors = {
    'background': '#252e3f',
    'text': '#7fafdf'
}


def second_div() -> html.Div:
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
    dff = df.copy().sort_values(NUM_CASOS, ascending=False)
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

app.layout = html.Div(
    id='root',
    children=[
        dcc.Tabs(
            id="tabs-with-classes",
            value='tab-2',
            parent_className='custom-tabs',
            className='custom-tabs-container',
            children=[
                dcc.Tab(
                    label='Tab one',
                    value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                dcc.Tab(
                    label='Tab two',
                    value='tab-2',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                dcc.Tab(
                    label='Tab three, multiline',
                    value='tab-3', className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
            ]
        ),

        html.Div(id='tabs-content-classes')
    ],
)


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
    df_graph = df_base.copy().drop(['CodigoIBGE'], axis=1).sort_values(DATA, ascending=True)
    df_graph = df_graph[df_graph[DATA] < '2020-08-01']

    df_graph['DATA'] = pd.to_datetime(df_graph[DATA], dayfirst=True).dt.month

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
        orientation='v'
    ))

    fig1.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[3, 4, 5, 6, 7, 8],
            title='Mës'
        ),
        yaxis=dict(
            title='Qtd. Infectados'
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
    df2 = df_base.copy()
    df2 = df2[df2[DATA] < '2020-08-01']

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
            title='Qtd. Infectados'
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
    Input(component_id='slider_top', component_property='value')
)
def update_progress(slctd):
    dff = df_base.copy().sort_values(NUM_CASOS, ascending=False)[[MUNICIPIO, DATA, NUM_CASOS]]
    dff[DATA] = pd.to_datetime(dff[DATA], dayfirst=True)
    dff = dff[dff[DATA] < '2020-08-01']

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


if __name__ == '__main__':
    app.run_server(debug=True)
