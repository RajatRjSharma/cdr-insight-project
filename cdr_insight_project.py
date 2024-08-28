
import pandas as pd
import re
import webbrowser
import dash
import dash_html_components as html
from dash.dependencies import Input,Output
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_table as dt


project_name=None
app=dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])



def load_data():
    print("Start of load data")
    call_datan="Call_data.csv"
    service_datan="Service_data.csv"
    device_datan="Device_data.csv"
    
    
    global call_data
    global service_data
    global device_data
    call_data=pd.read_csv(call_datan)
    service_data=pd.read_csv(service_datan)
    device_data=pd.read_csv(device_datan)
    
    temp_list=sorted(call_data["date"].dropna().unique().tolist())
    global start_date_list
    start_date_list=[{"label":str(i) ,"value":str(i) }for i in temp_list]
    
    global end_date_list
    end_date_list=[{"label":str(i) ,"value":str(i) }for i in temp_list]
    
    temp_list1=["Hourly","Daywise","Weekly"]
    global report_type
    report_type=[{"label":str(i),"value":str(i)} for i in temp_list1 ]
    
    
    print("End of load data")
    

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")
    
    
def create_app_ui():
    main_layout=html.Div(
        [
            html.Div([ html.H1(id="Main_title",children="CDR Analysis with Insights"),
                                   html.Img(src="/assets/telecom.png")],className="Top"),
            html.Div([dcc.Tabs(id="Tabs", value="tab-1",children=[
                dcc.Tab(label="Call Analytics Tool",id="call_ana",value="tab-1",className="Tab1",children=[
                    html.Div([
        html.Div([
            html.Br(),
        html.Div([dcc.Dropdown(id="d1",options=start_date_list,placeholder="Select Starting Date",value = "2019-06-20",style={'font-family': 'Charcoal, sans-serif'}),
        dcc.Dropdown(id="d2",options=end_date_list,placeholder="Select Ending Date",value = "2019-06-25",style={'font-family': 'Charcoal, sans-serif'})],className="d1"),
        html.Div([dcc.Dropdown(id="d3",placeholder="Select Group",multi = True,style={'font-family': 'Charcoal, sans-serif'}),
        dcc.Dropdown(id="d4",options=report_type,placeholder="Select Report Type",value="Hourly",style={'font-family': 'Charcoal, sans-serif'})],className="d2") ]),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Hr(),
        
       ])]),
                dcc.Tab(label="Device Analytics Tool",id="device_ana",value="tab-2",className="Tab1",children=[
                    html.Div([
        html.Br(),
        html.Div(dcc.Dropdown(
        id='d5', 
        options=start_date_list,
        placeholder = "Select Date here",
        multi = True),className="d1"), 
        html.Br(),
        html.Br(),
        html.Hr(),
    
            ])]),
                dcc.Tab(label="Service Analytics Tool",id="service_ana",value="tab-3",className="Tab1",children=[
                    html.Div([
        html.Br(),
        html.Div(dcc.Dropdown(
        id='d6', 
        options=start_date_list,
        placeholder = "Select Date here",
        multi = True),className="d1"), 
        html.Br(),
        html.Br(),
        html.Hr(),
       
            ])]),
            ])],className="tab"),
            html.Div(dcc.Loading(html.Div(id="load",children="Graph,Card,Table",style={'font-family': 'Charcoal, sans-serif'})))],style={ 'background-color': 'rgb(66,196,247)', 'margin': '0px -10px 10px'}
            

        
        
        )
    
    return main_layout


def count_devices(data):
    
    device_dict = {"Polycom" :0,
    "Windows" : 0,
    "iphone" : 0,
    "Android" : 0,
    "Mac" : 0,
    "Yealink" : 0,
    "Aastra" : 0,
    "Others" : 0}
    
    
    
    reformed_data = data["UserDeviceType"].dropna().reset_index()
    for var in reformed_data["UserDeviceType"]:
        if re.search("Polycom", var) :
            device_dict["Polycom"]+=1
        elif re.search("Yealink", var):
            device_dict["Yealink"]+=1
        elif re.search("Aastra", var):
            device_dict["Aastra"]+=1
        
        elif re.search("Windows", var):
            device_dict["Windows"]+=1
        elif re.search("iPhone|iOS", var):
            device_dict["iphone"]+=1
        elif re.search("Mac", var):
            device_dict["Mac"]+=1
        elif re.search("Android", var):
            device_dict["Android"]+=1
            
        else:
            device_dict["Others"]+=1
    final_data = pd.DataFrame()
    final_data["Device"] = device_dict.keys()
    final_data["Count"] = device_dict.values()
    return final_data




def create_card(title, content, color):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, className="card-title"),
                html.Br(),
                html.Br(),
                html.H2(content, className="card-subtitle"),
                html.Br(),
                ]
        ),
        color=color, inverse=True
    )
    return(card)


@app.callback(
    Output("load","children"),
    [
     Input("Tabs", "value"),
     Input("d1","value"),
     Input("d2","value"),
     Input("d3","value"),
     Input("d4","value"),
     Input("d5","value"),
     Input("d6","value"),
     ]
    )
 
def update_ui(Tabs,start_date,end_date,group,report_type,device_date,service_date):
    print("Data type:",str(type(start_date)))
    print("Data:",str(start_date))
    print("Data type:",str(type(end_date)))
    print("Data:",str(end_date))
    print("Data type:",str(type(group)))
    print("Data:",str(group))
    print("Data type:",str(type(report_type)))
    print("Data:",str(report_type))
    
    if Tabs == "tab-1":
        
     
        
        call_analytics_data = call_data[ (call_data["date"]>=start_date) & (call_data["date"]<=end_date) ]
         
        if group  == [] or group is None:
           pass
        else:
           call_analytics_data = call_analytics_data[call_analytics_data["Group"].isin(group)]
         
    
    
        graph_data = call_analytics_data
        if report_type == "Hourly":
            graph_data = graph_data.groupby("hourly_range")["Call_Direction"].value_counts().reset_index(name = "count")
            x = "hourly_range"
            
            content = call_analytics_data["hourly_range"].value_counts().idxmax()
            title =  "Busiest Hour"
        
            
        elif report_type == "Daywise":
            graph_data = graph_data.groupby("date")["Call_Direction"].value_counts().reset_index(name = "count")
            x = "date"
            
            content = call_analytics_data["date"].value_counts().idxmax()
            title =  "Busiest Day"
            
        else:
            graph_data = graph_data.groupby("weekly_range")["Call_Direction"].value_counts().reset_index(name = "count")
            x = "weekly_range"
            
            content = call_analytics_data["weekly_range"].value_counts().idxmax()
            title =  "Busiest WeekDay"
            
           
    
        figure = px.area(graph_data, 
                         x = x, 
                         y = "count",
                         color = "Call_Direction",
                         hover_data=[ "Call_Direction", "count"], 
                         template = "plotly_dark")
        figure.update_traces(mode = "lines+markers")
      
      
      
 
        total_calls = call_analytics_data["Call_Direction"].count()
        card_1 = create_card("Total Calls",total_calls, "success")
          
        incoming_calls = call_analytics_data["Call_Direction"][call_analytics_data["Call_Direction"]=="Incoming"].count()
        card_2 = create_card("Incoming Calls", incoming_calls, "primary")
          
        outgoing_calls = call_analytics_data["Call_Direction"][call_analytics_data["Call_Direction"]=="Outgoing"].count()
        card_3 = create_card("Outgoing Calls", outgoing_calls, "primary")
          
        missed_calls = call_analytics_data["Missed Calls"][call_analytics_data["Missed Calls"] == 19].count()
        card_4 = create_card("Missed Calls", missed_calls, "danger")
          
        max_duration = call_analytics_data["duration"].max()
        card_5 = create_card("Max Duration", f'{max_duration} min', "dark")
        
        card_6 = create_card(title, content, "primary")
             
      
    
        graphRow0 = dbc.Row([dbc.Col(id='card1', children=[card_1], ), dbc.Col(id='card2', children=[card_2], )])
        graphRow1 = dbc.Row([dbc.Col(id='card3', children=[card_3], ), dbc.Col(id='card4', children=[card_4], )])
        graphRow2 = dbc.Row([dbc.Col(id='card5', children=[card_5], ), dbc.Col(id='card6', children=[card_6], )])
     
        cardDiv = html.Div([graphRow0,html.Br(), graphRow1,html.Br(), graphRow2],className="card")
        
    
    
    
    
    
        datatable_data = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])["Call_Direction"].value_counts().unstack(fill_value = 0).reset_index()
        if call_analytics_data["Missed Calls"][call_analytics_data["Missed Calls"]==19].count()!=0:
            datatable_data["Missed Calls"] = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])["Missed Calls"].value_counts().unstack()[19]
        else:
            datatable_data["Missed Calls"] = 0
            
        datatable_data["Total_call_duration"] = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])["duration"].sum().tolist()
        
      
    
        datatable = html.Div(dt.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in datatable_data.columns],
        data=datatable_data.to_dict('records'),
        page_current=0,
        page_size=5,
        page_action='native',
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        }
        ),className="dtt")
        
            
        return [
                html.Div(dcc.Graph(figure = figure),className="graph"), 
                html.Br() ,
                cardDiv, 
                html.Br(),
                datatable
               ]
    
    elif Tabs == "tab-2":
        if device_date is None or device_date == []: 
            device_analytics_data = count_devices(device_data)
        else:
            device_analytics_data = count_devices(device_data[device_data["DeviceEventDate"].isin(device_date)])
          
        fig = px.pie(device_analytics_data, names = "Device", values = "Count", color = "Device", hole = .3,template = "plotly_dark")
        fig.update_layout(autosize=True,
                          margin=dict(l=0, r=0, t=25, b=20),
                          )
        return html.Div(dcc.Graph(figure = fig),className="graph")
    
    
    
    
    elif Tabs == "tab-3":
        if service_date is None or service_date == []:
            service_analytics_data = service_data["FeatureName"].value_counts().reset_index(name = "Count")
        else:
            service_analytics_data = service_data["FeatureName"][service_data["FeatureEventDate"].isin(service_date)].value_counts().reset_index(name = "Count")
        fig = px.pie(service_analytics_data, names = "index", values = "Count",color = "index",template = "plotly_dark")
        
        fig.update_layout(autosize=True,
                          margin=dict(l=0, r=0, t=25, b=20),
                          )
        return html.Div(dcc.Graph(figure = fig),className="graph")
    
    else:
        return None
    


@app.callback(
    Output("d3","options"),
    [
     Input("d1","value"),
     Input("d2","value")
     ]
    )

def update_group(start_date,end_date):
    reformed_data=call_data[(call_data["date"]>=start_date)&(call_data["date"]<=end_date)]
    group_list = reformed_data["Group"].unique().tolist()
    group_list = [{"label":m,"value": m} for m in group_list]
    return group_list



def main():
    print("Start of main")
    load_data()
    open_browser()
    
    global project_name
    project_name="New Telecom Project"
    global app
    app.layout=create_app_ui()
    app.title="CDR Analysis with Insights"
    app.run_server()
    
    print("end of main")
    project_name=None
    global call_data,service_data,device_data,start_date_list,end_date_list,report_type
    call_data=None
    service_data=None
    device_data=None
    start_date_list=None
    end_date_list=None
    report_type=None
    app=None

print("outer")

if __name__=='__main__':
    main()
