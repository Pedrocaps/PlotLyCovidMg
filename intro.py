import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import tab_1

app = dash.Dash(__name__, suppress_callback_exceptions=True)

data_obj = pd.read_csv("os_unificada_pendente.csv", delimiter=';')

tabs = [
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
        label='Filters',
        value='tab-3', className='custom-tab',
        selected_className='custom-tab--selected'
    ),
]

app.layout = html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-2',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=tabs),

    html.Div(id='tabs-content-classes')
]
)

tab_1_obj = tab_1.FirstTab(data_obj, app)
tab1 = tab_1_obj.get_tab()


def get_slider():
    return dcc.Slider(
        id='slider-updatemode',
        min=5,
        max=40,
        step=None,
        value=10,
        marks={
            5: '5',
            10: '10',
            20: '20',
            30: '30',
            40: 'Todos'
        },
    )


def get_remove_services():
    return dcc.Dropdown(
        id='dd_remove_service',
        options=[],
        multi=True,
        placeholder="Remover serviços",
    )


def get_select_type():
    list_type = data_obj['tipo_os'].unique().tolist()

    opt_list = [
        {'label': i, 'value': i} for i in list_type
    ]

    opt_values = [i for i in list_type]

    return dcc.Checklist(
        id='checklist_type',
        options=opt_list,
        value=opt_values
    )


tab2 = html.Div([
    html.H1(children="Top", style={'text-align': 'center'}, id='top_title'),
    get_select_type(),
    html.Br(),
    get_remove_services(),
    html.Br(),
    get_slider(),
    html.Br(),
    dcc.Graph(id='top_10', figure={})

],
    style={"border": "2px black solid"})


@app.callback([Output('top_10', 'figure'),
               Output('top_title', 'children'),
               Output('dd_remove_service', 'options')],
              [Input('slider-updatemode', 'value'),
               Input('slider-updatemode', 'max'),
               Input('dd_remove_service', 'value'),
               Input('checklist_type', 'value')])
def display_value(value, max, mult_values, type_value):
    dff = data_obj.copy()
    if type_value:
        dff = dff[dff['tipo_os'].isin(type_value)]

    dff = dff[['descricao_servico', 'codigo_servico']]
    if mult_values:
        dff = dff[~dff['descricao_servico'].isin(mult_values)]

    dff = dff.groupby(['descricao_servico'])[['codigo_servico']].count().sort_values('codigo_servico', ascending=False)
    dff = dff.reset_index()

    if value != max:
        dff = dff.head(value)
        text = f'Top {len(dff)} serviços'
    else:
        text = f'Todos os {len(dff)} serviços'

    bar_plt = px.bar(
        dff,
        x=dff['descricao_servico'],
        y=dff['codigo_servico']
    )

    # proporcional ao value selecionado ini
    tot_serv_prop = dff['codigo_servico'].sum()
    max_prop = dff['codigo_servico'][0]

    dff['cumsum_val'] = dff['codigo_servico'].cumsum()
    dff['cumsum_val_perc'] = dff['codigo_servico'].cumsum() / tot_serv_prop
    dff['cumsum_val_perc'] = dff['cumsum_val_perc'].astype(float).map("{:.2%}".format)
    dff['cumsum_val_propor'] = (dff['codigo_servico'].cumsum() / tot_serv_prop) * max_prop

    bar_plt.add_scatter(
        x=dff['descricao_servico'],
        y=dff['cumsum_val_propor'],
        name='Acc. Prop.',
        mode="lines+text",
        textposition="bottom right",
        hoverinfo='none',
        text=dff['cumsum_val_perc']

    )
    # proporcional ao value selecionado fim

    opt_list = [
        {'label': i, 'value': i} for i in dff['descricao_servico']
    ]

    return bar_plt, text, opt_list


@app.callback(Output('tabs-content-classes', 'children'),
              [Input('tabs-with-classes', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1
    elif tab == 'tab-2':
        return tab2
    elif tab == 'tab-3':
        return tab1


if __name__ == '__main__':
    app.run_server(debug=True)
