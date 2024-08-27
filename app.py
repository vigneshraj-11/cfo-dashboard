import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Montserrat&display=swap',
     dbc.themes.BOOTSTRAP
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,use_pages=True)

app.layout =dbc.Container(
    children=[
        # main app framework
        dbc.Row([
            dbc.Col(html.Img(src="assets/newlogo.png",style={'height':'50px'}),width=3),
            dbc.Col("Hospital Analytical Dashboard", style={'fontSize':30, 'textAlign':'center','color':'aliceblue'},
                    width=6),
            dbc.Col(width=3)
        ]),

        html.Div([
                dcc.Link(page['name'], href=page['path'],style={'color':'aliceblue','font-weight':'bold','textDecoration':'None'})
                for page in dash.page_registry.values()
            ],style={'text-align':'center'}),


        dash.page_container
    ],style={'background-color':'#151e26'},
 fluid=True)

# app.layout = html.Div(
#     [
#         # main app framework
#         html.Div([
#             html.Div(html.Img(src="assets/newlogo.png")),
#             html.Div("Hospital Analytical Dashboard", style={'fontSize':30, 'textAlign':'center','color':'aliceblue'}),
#             html.Div([
#                 dcc.Link(page['name'], href=page['path'],style={'color':'aliceblue','font-weight':'bold'})
#                 for page in dash.page_registry.values()
#             ],style={'text-align':'center'}),
#     ],style={'background-color':'#151e26'}),

#         dash.page_container
#     ],style={'background-color':'#151e26'}
# )


if __name__ == '__main__':
    app.run_server(debug=True, port=2024)