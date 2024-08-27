import dash                              # pip install dash
from dash import html,dcc,callback,State
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input 
import pandas as pd
from dash.exceptions import PreventUpdate
from numerize import numerize
import plotly.express as px    
import plotly.graph_objects as go
import datetime
# import seaborn as sns

colors = {
    'background': '#FFFBFB'
}

dash.register_page(__name__,path='/',name='Revenue & Profit Analysis')
config={
    'displayModeBar':False
}
#Datasets
df_bed = pd.read_excel('./data/bed_occupancy_new.xlsx')
# df_rev = pd.read_excel('./data/revOccupiedperSeat (1).xlsx')
# df_rev_1 = pd.read_excel('./data/Department_wiseRevenue.xlsx')
df_rev = pd.read_excel('./data/RevOccupiedSeat_Sun.xlsx')
df_rev_final = pd.read_excel('./data/TotalRevenue1 (2).xlsx')
df_budget = pd.read_excel("./data/budgetallocation.xlsx")
df_cashinflow = pd.read_excel("./data/cashflow.xlsx",sheet_name='Sheet1')

locations = df_rev_final.Location.unique()
year = df_rev_final.Year.unique()
month = df_rev_final.Month.unique()
quarter = df_rev_final.Quarter.unique()
departments = df_rev_final.Department.unique()
# Static charts ends
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H5('Filter', style={'textAlign':'center', 'color':'#FFF'}),
            html.Div([
                html.H6('City',style={'color':'#FFF'}),
                dcc.Dropdown(id='city', options=[
                    {'label':i, 'value':i} for i in locations
                ], value=['Chennai', 'Hyderabad', 'Mumbai', 'Bengaluru'],
                style={'fontSize':'10px'},
                multi=True)
            ]),
            html.Div([
                html.H6('Year', style={'color':'#FFF'}),
                dcc.Dropdown(id='year', options=[
                    {'label':i,'value':i} for i in year
                ],value=[2020,2021,2022],style={'fontSize':'10px'},multi=True)
            ],style={'margin-top':'4px'}),
            html.Div([
                html.H6('Quarter', style={'color':'#FFF'}),
                dcc.Dropdown(id='quarter', options=[
                    {'label':i,'value':i} for i in quarter
                ],value=['Q1','Q2','Q3','Q4'],style={'fontSize':'10px'},multi=True)
            ],style={'margin-top':'4px'}),
        
            html.Div([
                html.H6('Month', style={'color':'#FFF'}),
                dcc.Dropdown(id='month',options=[
                    {'label':i,'value':i} for i in month
                    
                ],value=['Jan', 'Feb', 'Mar', 'Apr','Nov', 'Dec','May','Jun','Jul','Aug','Sep','Oct'],style={'fontSize':'10px'},multi=True)
            ],style={'margin-top':'4px'}),
             html.Div([
                html.H6('Department', style={'color':'#FFF'}),
                dcc.Dropdown(id='dept',options=[
                    {'label':i,'value':i} for i in departments
                ],value=['Cardiology','Oncology','Pediatrics','Orthopedics'],
                style={'fontSize':'10px'},multi=True)
            ],style={'margin-top':'4px'}),
            html.Hr(),
            html.Div([
                dbc.Button('Submit',id='filter-val',n_clicks=0,type='button',color='primary',class_name='me-1',
                style={
                        'border-radius':'5px', 
                        'width':'150px',
                        'padding-bottom':'5px',
                        'textAlign': 'center',
                        }),
            ],style={'textAlign':'center'})
            

        ],width=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Revenue',style={'margin':'0px','font-weight':'Bold'}),
                            html.H2(id='revenue',children='000',style={'margin':'0px'})
                        ],style={'textAlign':'center', 'padding':'8px 4px 8px 4px'})
                     ],style={ 'padding':'0px 4px 0px 4px'}),
                ],width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Expense',style={'margin':'0px','font-weight':'Bold'}),
                            html.H2(id='expense',children='000',style={'margin':'0px'})
                        ],style={'textAlign':'center', 'padding':'8px 4px 8px 4px'})
                     ],style={ 'padding':'0px 4px 0px 4px'}),
                ],width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Profit',style={'margin':'0px','font-weight':'Bold'}),
                            html.H2(id='profit',children='000',style={'margin':'0px'})
                         ],style={'textAlign':'center', 'padding':'8px 4px 8px 4px'})
                    ],style={ 'padding':'0px 4px 0px 4px'}),
                ],width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Budget',style={'margin':'0px','font-weight':'Bold'}),
                            html.H2(id='budget',children='000',style={'margin':'0px'})
                        ],style={'textAlign':'center', 'padding':'8px 4px 8px 4px'})
                     ],style={ 'padding':'0px 4px 0px 4px'}),
                ],width=3),
                
                
            ],class_name='mb-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Budget by Year',style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='budget-yr-bar',figure={}, config=config,style={'height':'225px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'250px'})
                ],width=6,style={'padding':'0px 2px 0px 2px'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Budget by Department',style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='budget-dept-bar',figure={}, config=config,style={'height':'225px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'250px'})
                ],width=6,style={'padding':'0px 2px 0px 2px'}),
            ],class_name='mb-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Cashflow in Last 6 Months',style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='cashflow',figure={}, config=config,style={'height':'225px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'250px'})
                ],width=6,style={'padding':'0px 2px 0px 2px'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Budget Variance',style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='budget-var-bar',figure={}, config=config,style={'height':'225px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'250px'})
                ],width=6,style={'padding':'0px 2px 0px 2px'}),
            ],class_name='mb-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('IP/OP Overall Revenue by Year',style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='bar-rev-ip-op',figure={}, config=config,style={'height':'225px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'250px'})
                ],width=6,style={'padding':'0px 2px 0px 2px'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('IP/OP Overall Revenue by Location',style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='bar-ip-op-loc',figure={}, config=config,style={'height':'225px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'250px'})
                ],width=6,style={'padding':'0px 2px 0px 2px'}),
            ],class_name='mb-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Overall Bed Occupied Summary',style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='sun-rev-ratio',figure={}, config=config,style={'height':'225px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'250px'})
                ],width=7,style={'padding':'0px 2px 0px 2px'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('IP/OP Overall Revenue by Department',style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='bar-ip-op-dept',figure={}, config=config,style={'height':'225px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'250px'})
                ],width=5,style={'padding':'0px 2px 0px 2px'}),
            ],class_name='mb-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Revenue by Department',style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='bar-rev',figure={}, config=config,
                                      style={'height':'175px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'200px'})
                 ],width=4,style={'padding':'0px 2px 0px 2px'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Revenue by Location',style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='bar-rev-loc',figure={}, config=config,style={'height':'175px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'200px'})
                ],width=4,style={'padding':'0px 2px 0px 2px'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Revenue by Year',style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='bar-rev-year',figure={}, config=config,style={'height':'170px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'200px'})
                 ],width=4,style={'padding':'0px 2px 0px 2px'}),
            ],class_name='mb-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Ratio of beds occupied by Location',
                                    style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='bar-bed-ratio',figure={}, config=config,style={'height':'175px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'200px'})
                ],width=6,style={'padding':'0px 2px 0px 2px'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Ratio of beds occupied by Department',
                                    style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='bar-bed-ratio-loc',figure={}, config=config,style={'height':'175px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'200px'})
                ],width=6,style={'padding':'0px 2px 0px 2px'}),
               
            ],class_name='mb-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Avg. Revenue per seat by Location',
                                    style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='bar-rev-avg-loc',figure={}, config=config,style={'height':'175px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'200px'})
                ],width=6,style={'padding':'0px 2px 0px 2px'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Avg. Revenue per seat by Department',
                                    style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='bar-rev-avg-dept',figure={}, config=config,style={'height':'175px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'200px'})
                ],width=6,style={'padding':'0px 2px 0px 2px'}),
               
            ],class_name='mb-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Total Beds and Beds Occupied by Location',
                                    style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='bar-bed',figure={}, config=config,style={'height':'175px'})
                         ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'200px'})
                ],width=6,style={'padding':'0px 2px 0px 2px'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Total Beds and Beds Occupied by Department',
                                    style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='stack-bar-bed',figure={}, config=config,style={'height':'175px'})
                         ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'200px'})
                ],width=6,style={'padding':'0px 2px 0px 2px'}),
            ],class_name='mb-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Occupancy Rate by Department',
                                    style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='pie-bed',figure={}, config=config,style={'height':'235px'})
                        ],style={'padding':'2px 2px 0px 2px'})
                    ],style={'height':'260px'})
                ],width=5,style={'padding':'0px 2px 0px 2px'}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Beds Occupied by Department and Location',
                                    style={'textAlign':'center','margin':'0px','font-weight':'Bold'}),
                            dcc.Graph(id='heat-bed',figure={}, config=config, style={'height':'235px'} )
                        ],style={'padding':'2px 2px 0px 2px'})
                    ], style={'height':'260px'})
                ],width=7,style={'padding':'0px 2px 0px 2px'})
            ],class_name='mb-2'),
            

        ], width=10)
    ])
],fluid=True)

@callback(
    Output('revenue','children'),
    Output('budget','children'),
    Output('expense','children'),
    Output('profit','children'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def cards(n,city,year,quarter,dept,month):

    df_c = df_rev_final.copy()
    df_c1 = df_budget.copy()
    df2 = df_c1[(df_c1.Year.isin(year)) & (df_c1.Sector.isin(dept))]
    df1 = df_c[(df_c.Year.isin(year)) & (df_c.Month.isin(month)) & (df_c.Location.isin(city)) & (df_c.Department.isin(dept)) ]
    # df_r = df_r[(df_r['month'].isin(month)) & (df_r.state.isin(city)) & (df_r.year.isin(year))]
    revenue = numerize.numerize(sum(df1['Revenue']))
    expense = numerize.numerize(sum(df1['Expenses']))
    profit = numerize.numerize(sum(df1['Profit']))
    # location = len(df['Locations'].unique())
    budget = numerize.numerize(sum(df2['Budget Amount (in INR)']))
    department = len(df1['Department'].unique())
    return revenue,budget,expense,profit

@callback(
    Output('bar-bed','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_bed(n,city,year,quarter,dept,month,):
    df = df_bed.copy()
  
    df1 = df[(df.Department.isin(dept)) & (df.Locations.isin(city))]
    
    gp_df = df1.groupby(by=['Department']).agg({'Total Beds':'sum','Beds Occupied':'sum'}).reset_index()

    fig_bar = go.Figure(data=[
        go.Bar(name='Total Beds', x=gp_df['Department'],y=gp_df['Total Beds'], text=gp_df['Total Beds'] ),
        go.Bar(name='Beds Occupied', x=gp_df['Department'],y=gp_df['Beds Occupied'],text=gp_df['Beds Occupied'] ),
    ])
    fig_bar.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False},
                           title_x=0.5, font=dict(size=10),
                           margin=dict(l=20, r=20, t=30, b=5),plot_bgcolor = colors['background'],showlegend=False )
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_traces(texttemplate='%{text:.2s}')
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_layout(barmode='group')
    return fig_bar

@callback(
    Output('stack-bar-bed','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def stack_bar_bed(n,city,year,quarter,dept,month):
    df = df_bed.copy()
    df1 = df[(df.Department.isin(dept)) & (df.Locations.isin(city))]
    gp_df = df1.groupby(['Department', 'Locations']).agg({'Beds Occupied':'sum'}).reset_index()

    fig = px.bar(gp_df, x='Department',y='Beds Occupied',color='Locations',text_auto=True)
    fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],
            font=dict(size=10),showlegend=False,xaxis={'visible':True,'title':''},
            yaxis={'title':'', 'visible':False},
    )
    fig.update_traces(textfont_size=10, textangle=0, textposition="inside", cliponaxis=False)
        # fig_bar = go.Figure(data=[
    #     go.Bar(name='Total Beds', x=gp_df['Department'],y=gp_df['Beds Occupied']
    #            ,marker=dict(color=colors1), text=gp_df['Beds Occupied'] ),
    #     go.Bar(name='Beds Occupied', x=gp_df['Department'],y=gp_df['Locations'],
    #            text=gp_df['Locations'],marker=dict(color=colors1) ),
    # ])
    # fig_bar.update_layout(
    #                       xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
    #                       title_x=0.5, font=dict(size=10),
    #                        margin=dict(l=20, r=20, t=30, b=5),plot_bgcolor = colors['background'],showlegend=False )
    # fig_bar.update_yaxes(tickangle=45)
    # fig_bar.update_traces(texttemplate='%{text:.2s}')
    # fig_bar.update_coloraxes(showscale=False)
    # fig_bar.update_layout(barmode='stack')
    return fig

@callback(
    Output('pie-bed','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def pie_bed(n,city,year,quarter,dept,month):
    df = df_rev.copy()
    print(dept,'line376')
    df1 = df[(df.Department.isin(dept)) & (df.Location.isin(city))]
    grouped = df1.groupby('Department').agg({'Bed Occupied':'sum'}).reset_index()
    fig = px.pie(grouped,values=grouped['Bed Occupied'],names=grouped['Department'])
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=0),title_x=0.5,
                      font=dict(size=10),
                        legend=dict(orientation='h', yanchor='bottom',y=-0.27,xanchor='left',x=0.01))
   
    return fig

@callback(
    Output('heat-bed','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('dept','value'),
    State('year','value'),
    State('month','value')
)
def heat_bed(n,city,dept,year,month):

    df = df_bed.copy()
    df1 = df[(df.Locations.isin(city)) & (df.Department.isin(dept))]
    # df = df[(df.Locations.isin(city)) & (df.Department.isin(dept))]
    grouped = df1.groupby(['Department', 'Locations']).agg({'Beds Occupied':'sum'}).reset_index()

    fig = go.Figure(
        data=go.Heatmap(
            x=grouped['Locations'],
            y=grouped['Department'],
            z=grouped['Beds Occupied'],
            colorscale="Viridis",
        )
    )
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=0), font=dict(size=10),)
    # Set axis labels and title
    # fig.update_layout(

    #     title="Beds Occupied by Department and Location",
    # )

    return fig

@callback(
    Output('bar-rev','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_rev(n,city,year,quarter,dept,month):
    df = df_rev_final.copy()
    # df = df_rev.copy()
    df = df[(df.Location.isin(city)) & (df.Year.isin(year)) & (df.Quarter.isin(quarter)) & 
            (df.Department.isin(dept)) & (df.Month.isin(month))]
    gp_df = df.groupby(by=['Department']).agg({'Revenue':'sum','Expenses':'sum'}).reset_index()

    fig_bar = go.Figure(data=[
        go.Bar(name='Total Revenue', x=gp_df['Department'],y=gp_df['Revenue'], text=gp_df['Revenue'] ),
        go.Bar(name='Total Expense', x=gp_df['Department'],y=gp_df['Expenses'], text=gp_df['Expenses'] ),
        
    ])
    fig_bar.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),
                           margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],showlegend=False )
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_traces(texttemplate='%{text:.2s}')
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_layout(barmode='group')
    return fig_bar


@callback(
    Output('bar-rev-loc','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_rev_loc(n,city,year,quarter,dept,month):
    df = df_rev_final.copy()
    # df = df_rev.copy()
    df = df[(df.Location.isin(city)) & (df.Year.isin(year)) & (df.Quarter.isin(quarter)) & 
            (df.Department.isin(dept)) & (df.Month.isin(month))]
    gp_df = df.groupby(by=['Location']).agg({'Revenue':'sum','Expenses':'sum'}).reset_index()


    fig_bar = go.Figure(data=[
        go.Bar(name='Total Revenue by Location', x=gp_df['Location'],y=gp_df['Revenue'], text=gp_df['Revenue'] ),
        go.Bar(name='Total Expense by Location', x=gp_df['Location'],y=gp_df['Expenses'], text=gp_df['Expenses'] ),
        
    ])
    fig_bar.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),
                            margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],showlegend=False )
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_traces(texttemplate='%{text:.2s}')
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_layout(barmode='group')
    return fig_bar


@callback(
    Output('bar-rev-year','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_rev_year(n,city,year,quarter,dept,month):
    df = df_rev_final.copy()

    df = df[(df.Location.isin(city)) & (df.Year.isin(year)) & (df.Quarter.isin(quarter)) & 
            (df.Department.isin(dept)) & (df.Month.isin(month))]
    gp_df = df.groupby(by=['Year']).agg({'Revenue':'sum','Expenses':'sum'}).reset_index()
    # gp_df = df_rev.groupby(by=['Year']).agg({'Revenue':'sum'}).reset_index()

    fig_bar = go.Figure(data=[
        go.Bar(name='Total Revenue by Year', x=gp_df['Year'],y=gp_df['Revenue'], text=gp_df['Revenue'] ),
        go.Bar(name='Total Expense by Year', x=gp_df['Year'],y=gp_df['Expenses'], text=gp_df['Expenses'] ),
        
    ])
    fig_bar.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),
                            margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],showlegend=False )
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_traces(texttemplate='%{text:.2s}')
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_layout(barmode='group')
    return fig_bar

@callback(
    Output('bar-rev-avg-loc','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_rev_avg_loc(n,city,year,quarter,dept,month):
    df = df_rev.copy()
    df1 = df[(df.Department.isin(dept)) & (df.Location.isin(city))]

    gp_df = df1.groupby(by=['Location']).agg({'Revenue per Seat':'mean'}).reset_index()
    # gp_df = df_rev.groupby(by=['Location']).agg({'Revenue per Seat':'mean'}).reset_index()

    fig_bar = go.Figure(data=[
        go.Bar(name='Total Revenue by Year', x=gp_df['Location'],y=gp_df['Revenue per Seat'], text=gp_df['Revenue per Seat'] ),
        
    ])
    fig_bar.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),
                           margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],showlegend=False )
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_traces(texttemplate='%{text:.2s}')
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_layout(barmode='group')
    return fig_bar

@callback(
    Output('bar-rev-avg-dept','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_rev_avg_dept(n,city,year,quarter,dept,month):
    df = df_rev.copy()
    df1 = df[(df.Department.isin(dept)) & (df.Location.isin(city))]
    gp_df = df1.groupby(by=['Department']).agg({'Revenue per Seat':'mean'}).reset_index()

    fig_bar = go.Figure(data=[
        go.Bar(name='Total Revenue by Year', x=gp_df['Department'],y=gp_df['Revenue per Seat'], text=gp_df['Revenue per Seat'] ),
        
    ])
    fig_bar.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),
                           margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],showlegend=False )
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_traces(texttemplate='%{text:.2s}')
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_layout(barmode='group')
    return fig_bar

@callback(
    Output('bar-bed-ratio','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_bed_ratio(n,city,year,quarter,dept,month):
    df = df_rev.copy()
    df1 = df[(df.Department.isin(dept)) & (df.Location.isin(city))]
    gp_df = df1.groupby(by=['Location']).agg({'Bed Occupancy Ratio':'mean'}).reset_index()

    fig_bar = go.Figure(data=[
        go.Scatter( x=gp_df['Location'],y=gp_df['Bed Occupancy Ratio'], mode='lines+markers+text',
                   text=(gp_df['Bed Occupancy Ratio']*100).round().astype(str)+'%',
               textposition='middle right'),
        
    ])
    fig_bar.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),
                           margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],showlegend=False )
    fig_bar.update_yaxes(tickangle=45)
    # fig_bar.update_traces(texttemplate='%{text:.2s}')
    fig_bar.update_layout(yaxis_tickformat=".0%")
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_layout(barmode='group')
    return fig_bar

@callback(
    Output('bar-bed-ratio-loc','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_bed_ratio_loc(n,city,year,quarter,dept,month):
    df = df_rev.copy()
    df1 = df[(df.Department.isin(dept)) & (df.Location.isin(city))]
    gp_df = df1.groupby(by=['Department']).agg({'Bed Occupancy Ratio':'mean'}).reset_index()

    fig_bar = go.Figure(data=[
        go.Scatter( x=gp_df['Department'],y=gp_df['Bed Occupancy Ratio'], mode='lines+markers+text',
                   text=(gp_df['Bed Occupancy Ratio']*100).round(2).astype(str)+'%',
               textposition='middle right'),
        
    ])
    fig_bar.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),
                           margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],showlegend=False )
    fig_bar.update_yaxes(tickangle=45)
    # fig_bar.update_traces(texttemplate='%{text:.2s}')
    fig_bar.update_layout(yaxis_tickformat=".0%")
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_layout(barmode='group')
    return fig_bar

@callback(
    Output('sun-rev-ratio','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('month','value')
)
def sun_rev_ratio(n,city,year,month):
    df = df_rev.copy()
    df['Revenue per Seat'] = df['Revenue per Seat'].apply(lambda x: '{:.1f}k'.format(x/1000))
    fig = px.sunburst(df, path=['Year','Location', 'Department', 'Revenue per Seat'],color='Department',
                       color_discrete_map={'Cardiology': 'red', 'Oncology': 'green', 'Orthopedics': 'blue', 'Neurology': 'orange'},
                       hover_data={'Year': False, 'Location': False, 'Department': True, 'Revenue per Seat': True},
                       labels={'Revenue per Seat': 'Revenue per Seat (k)'}
                    )
    fig.update_layout(grid= dict(columns=2, rows=1),margin = dict(t=10, l=10, r=10, b=5), font=dict(size=10),)
    return fig

@callback(
    Output('bar-rev-ip-op','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_rev_opop(n,city,year,quarter,dept,month):
    df = df_rev_final.copy()
    # df = df_rev.copy()
    df = df[(df.Location.isin(city)) & (df.Year.isin(year)) & (df.Quarter.isin(quarter)) & 
            (df.Department.isin(dept)) & (df.Month.isin(month))]
    gp_df = df.groupby(by=['Year']).agg({'Inpatient Revenue':'sum','Outpatient Revenue':'sum'}).reset_index()

    fig_bar = go.Figure(data=[
        go.Bar(name='Total Revenue IP', x=gp_df['Year'],y=gp_df['Inpatient Revenue'], text=gp_df['Inpatient Revenue'] ),
        go.Bar(name='Total Revenue OP', x=gp_df['Year'],y=gp_df['Outpatient Revenue'], text=gp_df['Outpatient Revenue'] ),
        
    ])
    fig_bar.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),
                           margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],showlegend=False )
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_traces(texttemplate='%{text:.2s}')
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_layout(barmode='group')
    return fig_bar

@callback(
    Output('bar-ip-op-loc','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_rev_opop_loc(n,city,year,quarter,dept,month):
    df = df_rev_final.copy()
    # df = df_rev.copy()
    df = df[(df.Location.isin(city)) & (df.Year.isin(year)) & (df.Quarter.isin(quarter)) & 
            (df.Department.isin(dept)) & (df.Month.isin(month))]
    gp_df = df.groupby(by=['Location']).agg({'Inpatient Revenue':'sum','Outpatient Revenue':'sum'}).reset_index()

    fig_bar = go.Figure(data=[
        go.Bar(name='Total Revenue IP', x=gp_df['Location'],y=gp_df['Inpatient Revenue'], text=gp_df['Inpatient Revenue'] ),
        go.Bar(name='Total Revenue OP', x=gp_df['Location'],y=gp_df['Outpatient Revenue'], text=gp_df['Outpatient Revenue'] ),
        
    ])
    fig_bar.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),
                           margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],showlegend=False )
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_traces(texttemplate='%{text:.2s}')
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_layout(barmode='group')
    return fig_bar
@callback(
    Output('bar-ip-op-dept','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_rev_opop_dept(n,city,year,quarter,dept,month):
    df = df_rev_final.copy()
    # df = df_rev.copy()
    df = df[(df.Location.isin(city)) & (df.Year.isin(year)) & (df.Quarter.isin(quarter)) & 
            (df.Department.isin(dept)) & (df.Month.isin(month))]
    gp_df = df.groupby(by=['Department']).agg({'Inpatient Revenue':'sum','Outpatient Revenue':'sum'}).reset_index()

    fig_bar = go.Figure(data=[
        go.Bar(name='Total Revenue IP', x=gp_df['Department'],y=gp_df['Inpatient Revenue'], text=gp_df['Inpatient Revenue'] ),
        go.Bar(name='Total Revenue OP', x=gp_df['Department'],y=gp_df['Outpatient Revenue'], text=gp_df['Outpatient Revenue'] ),
        
    ])
    fig_bar.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),
                           margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],showlegend=False )
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_traces(texttemplate='%{text:.2s}')
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_layout(barmode='group')
    return fig_bar

@callback(
    Output('budget-yr-bar','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_bed(n,city,year,quarter,dept,month,):
    df = df_budget.copy()
    # df1 = df.loc[df['Year']==year[0]]
    df = df[(df.Year.isin(year)) & (df.Sector.isin(dept))]
    gp_df = df.groupby(by=['Year']).agg({'Actual Amount (in INR)':'sum','Budget Amount (in INR)':'sum'}).reset_index()

    fig = go.Figure(data=[
        go.Bar(name='Actual Amount', x=gp_df['Year'],y=gp_df['Actual Amount (in INR)'], 
               text=gp_df['Actual Amount (in INR)'] ),
        go.Bar(name='Budget Amount', x=gp_df['Year'],y=gp_df['Budget Amount (in INR)'], 
               text=gp_df['Budget Amount (in INR)'] ),
        
    ])

    fig.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),legend=dict(orientation='h',y=1.1,x=0.5),
                           margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],
                           showlegend=True )
   
    fig.update_traces(texttemplate='%{text:.2s}')
    fig.update_coloraxes(showscale=False)
    
    return fig

@callback(
    Output('budget-dept-bar','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_bed(n,city,year,quarter,dept,month,):
    df = df_budget.copy()
    # df1 = df.loc[df['Year']==year[0]]
    df = df[(df.Year.isin(year)) & (df.Sector.isin(dept))]
    gp_df = df.groupby(by=['Sector']).agg({'Actual Amount (in INR)':'sum','Budget Amount (in INR)':'sum'}).reset_index()

    fig = go.Figure(data=[
        go.Bar(name='Actual Amount', x=gp_df['Sector'],y=gp_df['Actual Amount (in INR)'], 
               text=gp_df['Actual Amount (in INR)'] ),
        go.Bar(name='Budget Amount', x=gp_df['Sector'],y=gp_df['Budget Amount (in INR)'], 
               text=gp_df['Budget Amount (in INR)'] ),
    ])

    fig.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),legend=dict(orientation='h',y=1.1,x=0.5),
                           margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],
                           showlegend=True )
   
    fig.update_traces(texttemplate='%{text:.2s}')
    fig.update_coloraxes(showscale=False)
    
    return fig

@callback(
    Output('budget-var-bar','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_bed(n,city,year,quarter,dept,month,):
    df = df_budget.copy()
    # df1 = df.loc[df['Year']==year[0]]
    # print(df1,'line859')
    df = df[(df.Year.isin(year)) & (df.Sector.isin(dept))]
    gp_df = df.groupby(by=['Sector']).agg({'Budget Variance (in INR)':'sum'}).reset_index()

    fig = go.Figure(data=[
        go.Bar( x=gp_df['Sector'],y=gp_df['Budget Variance (in INR)'], 
               text=gp_df['Budget Variance (in INR)'] ),
        
    ])
    fig.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),
                           margin=dict(l=10, r=10, t=10, b=0),plot_bgcolor = colors['background'],
                           showlegend=False )
   
    fig.update_traces(texttemplate='%{text:.2s}')
    # fig = px.bar(df1, x='Sector',y='Budget Variance (in INR)',color='Sector',
    #             labels=dict(index='Amount'))
    return fig

@callback(
    Output('cashflow','figure'),
    Input('filter-val','n_clicks'),
    State('city','value'),
    State('year','value'),
    State('quarter','value'),
    State('dept','value'),
    State('month','value')
)
def bar_bed(n,city,year,quarter,dept,month,):
    df_cash = df_cashinflow.copy()
    fig = px.line(df_cash, x='Date',y = "Cash Inflow (INR)", color='Category',
               labels=dict(Category='Cash Inflow Category', Amount='Cash Inflow (INR)'),
              line_shape='spline',line_group='Category',color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_layout(xaxis={'visible':True,'title':''},yaxis={'title':'', 'visible':False}, 
                          title_x=0.5, font=dict(size=10),margin=dict(l=10, r=10, t=10, b=0),
                          legend=dict(orientation='h', yanchor="top", y=1.2,xanchor='center', x=0.5, title=""),
                           plot_bgcolor = colors['background'],
                           showlegend=True )
    return fig
