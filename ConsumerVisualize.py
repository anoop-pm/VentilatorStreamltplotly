from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
import json
from kafka import KafkaConsumer
import pandas as pd
import warnings
import numpy as np
import plotly.express as px

# Configure the Kafka consumer
bootstrap_servers = 'localhost:9092'
topic_name = 'heartbeat'
placeholder = st.empty()

# Create the Kafka consumer
consumer = KafkaConsumer(topic_name, bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))

st.title(':blue[Ventilator Monitor Screen]')

st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 500px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)

plot_selection = st.sidebar.selectbox('Select Patient', ['Patient1', 'Patient2'])

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

# Initialize an empty list to store heartbeat values
heartbeats = []
# Continuously poll for new messages
messagelist = []
p1oxl=[]
p1pres=[]
p1vol=[]
p1fl=[]
p1heart=[]

p2oxl=[]
p2pres=[]
p2vol=[]
p2fl=[]
p2heart=[]


warnings.filterwarnings("ignore")

Scatter_Geo_Dataset =  pd.read_csv(r'Scatter_Geo_Dataset.csv')
Coropleth_Dataset =  pd.read_csv(r'vacineregister.csv')
Data_Map_population_df = pd.read_csv(r'coviddatadummy.csv')
Indian_States= pd.read_csv(r'Longitude_Latitude_State_Table.csv')
# Dynamic Scattergeo Data Generation
Transaction_scatter_districts = Data_Map_population_df.sort_values(by=['Place_Name'], ascending=False)
# -------------------------------------FIGURE1 INDIA MAP Covid Patient------------------------------------------------------------------

#scatter plotting the states codes
Indian_States = Indian_States.sort_values(by=['state'], ascending=False)
Indian_States['Registered_Users']=Coropleth_Dataset['Registered_Users']
Indian_States['Total_covid_count']=Data_Map_population_df['Total_covid_count']

fig=px.scatter_geo(Indian_States,
                    lon=Indian_States['Longitude'],
                    lat=Indian_States['Latitude'],
                    text = Indian_States['code'], #It will display district names on map
                    hover_name="state",
                    hover_data=["Total_covid_count"],
                    )
fig.update_traces(marker=dict(color="black" ,size=0.3))
fig.update_geos(fitbounds="locations", visible=False,)
fig1=px.scatter_geo(Scatter_Geo_Dataset,
                    lon=Scatter_Geo_Dataset['Longitude'],
                    lat=Scatter_Geo_Dataset['Latitude'],
                    color=Scatter_Geo_Dataset['col'],
                    size=Scatter_Geo_Dataset['Total_covid_count'],
                    #text = Scatter_Geo_Dataset['District'], #It will display district names on map
                    hover_name="District",
                    hover_data=["State","Total_covid_count"],
                    title='District',
                    size_max=22,)
fig1.update_traces(marker=dict(color="rgb(0, 0, 0)" ,line_width=1))    #rebeccapurple
#coropleth mapping india
fig_ch = px.choropleth(
                    Coropleth_Dataset,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='state',
                    color_continuous_scale='Reds',
                    color="Registered_Users"
                    )
fig_ch.update_geos(fitbounds="locations", visible=False,)

fig_ch.add_trace( fig.data[0])
fig_ch.add_trace(fig1.data[0])
st.sidebar.write("### **:PURPLE[Covid Today Status]**")
st.sidebar.plotly_chart(fig_ch, use_container_width=True)


def multiline(p,v,f):
    time = np.arange(0, 10, 0.1)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=time, y=p, mode='lines+markers', name='Pressure', line=dict(color='blue', width=2)))
    fig.add_trace(
        go.Scatter(x=time, y=v, mode='lines+markers', name='Volume', line=dict(color='green', width=2)))
    fig.add_trace(go.Scatter(x=time, y=f, mode='lines+markers', name='Flow', line=dict(color='orange', width=2)))
    # Configure the layout of the combined plot
    fig.update_layout(
        title='Ventilator Data',
        yaxis_title ="Rate",
        xaxis_title='Time {}'.format(now),
        template='plotly_dark'
    )

    # Display the combined plot
    return st.plotly_chart(fig)



def Heart(value,heartrate):
    st.write(f"Latest heartbeat: {value}")
    fig = go.Figure(data=go.Scatter(y=heartrate, mode='lines+markers'))
    fig.update_layout(
        title='Heart Rate',
        xaxis_title='Time {}'.format(now),
        yaxis_title='Heart Rate)',
        template='plotly_dark'
    )
    fig.update_traces(line=dict(color='red', width=2))
    return st.plotly_chart(fig, use_container_width=True)

def Pressure(value,pressure):
    st.write(f"Latest Pressure: {value}")
    fig = go.Figure(data=go.Scatter(y=pressure, mode='lines+markers'))
    fig.update_layout(
        title='Pressure',
        xaxis_title='Time {}'.format(now),
        yaxis_title='Heart Rate)',
        template='plotly_dark'
    )
    fig.update_traces(line=dict(color='orange', width=2))
    return st.plotly_chart(fig, use_container_width=True)

def Volume(value,volume):
    st.write(f"Latest Volume: {value}")
    fig = go.Figure(data=go.Scatter(y=volume, mode='lines+markers'))
    fig.update_layout(
        title='Pressure',
        xaxis_title='Time {}'.format(now),
        yaxis_title='Pressure Rate)',
        template='plotly_dark'
    )
    fig.update_traces(line=dict(color='yellow', width=2))
    return st.plotly_chart(fig, use_container_width=True)
def Flow(value,flow):
    st.write(f"Latest Flow: {value}")
    fig = go.Figure(data=go.Scatter(y=flow, mode='lines+markers'))
    fig.update_layout(
        title='Pressure',
        xaxis_title='Time {}'.format(now),
        yaxis_title='Flow Rate)',
        template='plotly_dark'
    )
    fig.update_traces(line=dict(color='green', width=2))
    return st.plotly_chart(fig, use_container_width=True)

def OxygenLevel(value,flow):
    st.write(f"Latest Oxygen: {value}")
    fig = go.Figure(data=go.Scatter(y=flow, mode='lines+markers'))
    fig.update_layout(
        title='Oxygen SpO2',
        xaxis_title='Time {}'.format(now),
        yaxis_title='Oxygen SpO2 Rate)',
        template='plotly_dark'
    )
    fig.update_traces(line=dict(color='white', width=2))
    return st.plotly_chart(fig, use_container_width=True)


def display_number_box(number):
    fig = go.Figure(go.Indicator(
        mode="number+gauge",
        value=number,
        gauge={
            'axis': {'visible': False},
            'bar': {'color': 'red'},
            'bgcolor': 'white',
            'borderwidth': 2,
            'bordercolor': 'gray',
            'steps': [
                {'range': [0, number], 'color': 'red'},
                {'range': [number, 10], 'color': 'lightgray'}
            ]
        }
    ))

    fig.update_layout(
        height=200,
        width=400,
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20)
    )

    return st.plotly_chart(fig)


for message in consumer:

    data = dict(message.value)
    p1data=data['Patient1']
    print(p1data)
    # {'Patient1': {'pressure': 14, 'volume': 196, 'flow': 95, 'oxygen': 0.8875063307980839, 'heartbeat': 69.71967316288092}}
    p1Pressure = p1data['pressure']
    p1pres.append(p1Pressure)
    p1volume = p1data['volume']
    p1vol.append(p1volume)
    p1flow = p1data['flow']
    p1fl.append(p1flow)
    p1oxygen = p1data['oxygen']
    p1oxl.append(p1oxygen)
    p1hb = p1data['heartbeat']
    p1heart.append(p1hb)

    p2data = data['Patient2']
    print(p2data)
    # {'Patient1': {'pressure': 14, 'volume': 196, 'flow': 95, 'oxygen': 0.8875063307980839, 'heartbeat': 69.71967316288092}}
    p2Pressure = p2data['pressure']
    p2pres.append(p1Pressure)
    p2volume = p1data['volume']
    p2vol.append(p1volume)
    p2flow = p1data['flow']
    p2fl.append(p1flow)
    p2oxygen = p1data['oxygen']
    p2oxl.append(p1oxygen)
    p2hb = p1data['heartbeat']
    p2heart.append(p1hb)


    # Plot the heartbeat values
    with placeholder.container():
        # Display the latest heartbeat value
        # Display the selected plot
        if plot_selection == 'Patient1':
            multiline(p1pres,p1vol,p1fl)
            tab1, tab2, tab3, tab4, tab5, = st.tabs(["Heart Rate", "Pressure", "Volume", "Flow", "Oxygen"])

            with tab1:
                Heart(p1hb, p1heart)
                display_number_box(p1hb)
            with tab2:
                Pressure(p1Pressure, p1pres)
                display_number_box(p1Pressure)
            with tab3:
                Volume(p1volume, p1vol)
                display_number_box(p1volume)
            with tab4:
                Flow(p1flow, p1fl)
                display_number_box(p1flow)
            with tab5:
                OxygenLevel(p1oxygen, p1oxl)
                display_number_box(p1oxygen)

        elif plot_selection == 'Patient2':
            multiline(p2pres, p2vol, p2fl)
            tab1, tab2, tab3, tab4, tab5, = st.tabs(["Heart Rate", "Pressure", "Volume", "Flow", "Oxygen"])
            with tab1:
                Heart(p2hb, p2heart)
                display_number_box(p2hb)
            with tab2:
                Pressure(p2Pressure, p2pres)
                display_number_box(p2Pressure)
            with tab3:
                Volume(p2volume, p2vol)
                display_number_box(p2volume)
            with tab4:
                Flow(p2flow, p2fl)
                display_number_box(p2flow)
            with tab5:
                OxygenLevel(p2oxygen, p2oxl)
                display_number_box(p2oxygen)







