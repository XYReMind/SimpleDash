import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go
from plotly.graph_objs import *
import pandas as pd

app =dash.Dash()

#map token
mapbox_access_token = 'pk.eyJ1Ijoia3JpcmlyaWkiLCJhIjoiY2prMm41NzBzMHUyNzNxcWxlYXRoNDR6cyJ9.u2O_firbAzFF_cer99hznA'

df_job = pd.read_csv("job_to_map.csv")
del df_job["Unnamed: 0"]
df_job['text'] = df_job['name'] + '<br> ' + 'Company：' +(df_job['company']).astype(str)+ '<br> ' +'Stars'+ (df_job['final_score']).astype(int).astype(str)
colors = ["red","rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","green","rgb(138 ,43, 226)","rgb(47 ,79 ,79)",
         "#26CC58", "#28C86D", "#29C481", "#2AC093", "#2BBCA4","#613099","#F4EC15", "#DAF017", "#BBEC19", "9DE81B"]


#this is the main part of the map, use callback to get it
def get_figure(values):
    datas = []
    #need the lon lat
    job = Data([Scattermapbox(
        lon=df_job['lon'],
        lat=df_job['lat'],
        mode='markers',
        marker=Marker(
            color=colors[4], #marker's color
        ),
        text=df_job['text'], #content's show on marker
        name = "job"
    )
    ])
    house = job
    trans = {"job": job,"house":house}
    for item in values:
        datas.extend(trans[item])
    # Display data
    layout = Layout(
        autosize=True,
        height=600,  #the width of the map
        width=1100,
        margin=Margin(l=10, r=10, t=20, b=20),
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=39.908543,  #open the centre of the map
                lon=116.397389
            ),
            pitch=0,
            zoom=10,
            style='mapbox://styles/mapbox/streets-v10'  #the type of the map
        ),
    )
    return go.Figure(data=datas, layout=layout)

NAME ='find a job'
INFO ="Find the best fitting job in Beijing!"

app.layout = html.Div([
    #set the title
    html.H1(
        children='Find the best fitting job in Bejing',
        style={
            'textAlign': 'center',
            'color': colors[5],
            'fontSize':'30px'
        }
    ),
    #sub title
    html.Div(children='Find the best job for you:)',
        style={
        'textAlign': 'center',
        'color': colors[5],
        'fontSize':'18px'
    }),
    #check box
    html.Div([
         html.Div([
             dcc.Checklist(
                 id ='checkbox',
                 options=[
                     {'label': u'JOB', 'value': 'job'},
                     {'label': u'HOUSE', 'value': 'house'},
                 ],
                 values=['job','house'])
         ],className='twelve columns',style=dict( textAlign='center',columnCount=8,color=colors[6])),
    ]),
    #to show thw details
    html.Div([
        html.Div([
            html.Br(),
            # name of the job
            html.A(NAME,
                  id='chem_name',
                  href="http://blog.csdn.net/tonydz0523",
                  target="_blank"),
            html.Br(),
            # company name
            html.A(NAME,
                  id='company_name',
                  href="http://blog.csdn.net/tonydz0523",
                  target="_blank",
                  style = dict( maxWidth="350px")),
            # detail of the job
            html.Div(INFO,
                id ='chem_desc',
                style = dict( maxHeight='500px',maxWidth="350px", fontSize='13px' )),
            ],className ='three columns',style=dict(height='500px',textAlign='center')),
        #call the information to the function
        html.Div([
            dcc.Graph(id="histogram",
                    style=dict(width='1100px'),
                    hoverData=dict( points=[dict(pointNumber=10)])
                    ),
        ], className='eight columns')
    ])
])
#get the map
@app.callback(Output('histogram', "figure"),
              [Input("checkbox", "values")])
def update_graph(values):
    return get_figure(values)
#get the job name
@app.callback(
    Output('chem_name', 'children'),
    [Input('histogram', 'hoverData')])
def get_hover_title(hoverData):
    try:
        name = str(hoverData).split("<")[0].split("'")[-1]
        company = str(hoverData).split("<")[1].split("：")[1]
        info = df_job[df_job['name'].isin([name])]
        info = info[info["company"].isin([company])]
        title = info["name"].tolist()[0]
        return title
    except :
        pass
#get the link of the job
@app.callback(
    dash.dependencies.Output('chem_name', 'href'),
    [dash.dependencies.Input('histogram', 'hoverData')])
def return_href(hoverData):
    try:
        name = str(hoverData).split("<")[0].split("'")[-1]
        company = str(hoverData).split("<")[1].split("：")[1]
        info = df_job[df_job['name'].isin([name])]
        info = info[info["company"].isin([company])]
        link = info['link'].tolist()[0]
        return link
    except Exception as e:
        print(e)
# get the name of the company
@app.callback(
    Output('company_name', 'children'),
    [Input('histogram', 'hoverData')])
def get_hover_title(hoverData):
    try:
        name = str(hoverData).split("<")[0].split("'")[-1]
        company = str(hoverData).split("<")[1].split("：")[1]
        info = df_job[df_job['name'].isin([name])]
        info = info[info["company"].isin([company])]
        title = info["company"].tolist()[0]
        return title
    except :
        pass
#get the link of the job
@app.callback(
    dash.dependencies.Output('company_name', 'href'),
    [dash.dependencies.Input('histogram', 'hoverData')])
def return_href(hoverData):
    try:
        name = str(hoverData).split("<")[0].split("'")[-1]
        company = str(hoverData).split("<")[1].split("：")[1]
        info = df_job[df_job['name'].isin([name])]
        info = info[info["company"].isin([company])]
        link = info['url'].tolist()[0]
        return link
    except Exception as e:
        print(e)
#get the details of the job
@app.callback(
    Output('chem_desc', 'children'),
    [Input('histogram', 'hoverData')])
def display_molecule(hoverData):
    try:
        name = str(hoverData).split("<")[0].split("'")[-1]
        company = str(hoverData).split("<")[1].split("：")[1]
        info = df_job[df_job['name'].isin([name])]
        info = info[info["company"].isin([company])]
        description = info["info"].tolist()[0]
        return description
    except:
        pass


if __name__ == '__main__':
    # run the dashboard
    app.run_server(debug=True)
