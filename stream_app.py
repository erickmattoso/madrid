# import datetime
from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def plot_figure(my_df):
    fig = go.Figure(go.Scattermapbox(
        mode="markers",
        hovertext=["Hotel"],
        hoverinfo='text',
        lon=[-3.670566],
        lat=[40.3961208],
        marker={"size": 25}))
    
    fig.add_trace(go.Scattermapbox(
        mode="markers+lines",
        hovertext=list(my_df.title),
        hoverinfo='text',
        lon=my_df.lng,
        lat=my_df.lat,
        marker={
            'color': 'green',
            'size': 15,
            'opacity': 0.9
        }))
    
    done = my_df[my_df["status"]=="Done"]
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        hovertext=list(done.title),
        hoverinfo='text',
        lon=done.lng,
        lat=done.lat,
        marker={
            'color': 'red',
            'size': 15,
            'opacity': 0.9
        }))

    try:
        fig.add_trace(go.Scattermapbox(
            lon=[result.get("GET_LOCATION")["lon"]],
            lat=[result.get("GET_LOCATION")["lat"]],
            marker={"size": 15})
        )
    except:
        pass

    fig.update_layout(
        showlegend=False,
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        mapbox={
            "center": {"lon": my_df["lng"].mean(), "lat": my_df["lat"].mean()},
            "style": "carto-positron",
            "zoom": 11.8})
    return fig
    
def extractCoords(input):
    coords = []
    for item in input:
        coords.append((float(item["lat"]), float(item["lng"])))
    return coords

def compute_euclidean_distance_matrix(locations):
    size = len(locations)
    distances = [[0 for x in range(size)] for y in range(size)]
    scalar = 10000
    for from_counter, from_node in enumerate(locations):
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                x_d = (from_node[0] - to_node[0])*scalar
                y_d = (from_node[1] - to_node[1])*scalar
                distances[from_counter][to_counter] = int(math.hypot(x_d, y_d))
    return distances

def create_data_model(csvfile):
    places =  csvfile.to_dict('records') #parseCSV(csvfile)
    coords = extractCoords(places)
    distancem = compute_euclidean_distance_matrix(coords)
    data = {}
    data["places"] = places
    data["distance_matrix"] = distancem
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data

def print_solution_gmaps(manager, routing, assignment, data, val=[]):
    index = routing.Start(0)
    while not routing.IsEnd(index):
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        list_lat = data["places"][manager.IndexToNode(index)]["lat"]
        list_long = data["places"][manager.IndexToNode(index)]["lng"]
        list_title = data["places"][manager.IndexToNode(index)]["title"]
        list_status = data["places"][manager.IndexToNode(index)]["status"]
        val.append([list_lat, list_long, list_title,list_status])
    return val

def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data_model["distance_matrix"][from_node][to_node]

st.title('Trip to Madrid')
loc_button = Button(label="Get Location")
loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition(
        (loc) => {
            document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
        }
    )
    """))
result = streamlit_bokeh_events(
    loc_button,
    events="GET_LOCATION",
    key="get_location",
    override_height=40,
    debounce_time=0)

df_original = pd.read_csv('csv_csv.csv', index_col=[0])

custom_col_0 = st.columns((1, 1))

fill = custom_col_0[0].selectbox("Filter day", options=df_original.columns[4:])
df_entrada = df_original[df_original[fill].notna()].sort_values(fill)
my_expander = st.expander(label='Advanced Filters')
with my_expander:
    yyyyy = st.multiselect("Filter Places",options=list(df_entrada['title']),default=list(df_entrada['title']))
    itovisit = st.checkbox("To Visit")
    if itovisit:
        done = df_entrada[df_entrada["status"]!="Done"]
        yyyyy = list(done['title'])
    df_entrada=df_entrada[df_entrada["title"].isin(yyyyy)]
    custom_col_1 = st.columns((.5, 1, .5))
    custom_col_1[0].write("Calculate route")
    if custom_col_1[0].button("calculate"):
        data_model = create_data_model(df_entrada)
        manager = pywrapcp.RoutingIndexManager(len(data_model["distance_matrix"]), data_model["num_vehicles"], data_model["depot"])
        routing = pywrapcp.RoutingModel(manager)
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.seconds = 30
        assignment = routing.SolveWithParameters(search_parameters)
        val = print_solution_gmaps(manager, routing, assignment, data_model)
        val.append(val[0])
        df_entrada = pd.DataFrame(val)
        df_entrada.columns ="lat","lng","title","status"
        st.session_state.df_entrada = df_entrada

    column = custom_col_1[1].text_input("Name of Route")
    custom_col_1[2].write("Click to Save Route")
    if custom_col_1[2].button("Save As"):
        df_entrada = st.session_state.df_entrada.reset_index()
        new = df_entrada[["title","index"]]
        new.columns = "title",column
        df_original = pd.merge(df_original,new,on="title",how="left")
        df_original.to_csv("csv_csv.csv", index=[0])

fig = plot_figure(df_entrada)
st.plotly_chart(fig, use_container_width=True)
custom_col_2 = st.columns((2, 1, .5))
mylist = df_entrada['title']+" (" + df_entrada['status']+") "
place = custom_col_2[0].selectbox("Status", options=list(mylist))[:-8]
sts = custom_col_2[1].selectbox("Status", options=("Done", "ToDo"))
if custom_col_2[2].button("Update"):
    df_entrada.loc[df_entrada["title"].str.contains(place), "status"] = sts    
    df_entrada.to_csv('csv_csv.csv', index=[0])
    custom_col_2[2].markdown("Saved!")
    st.experimental_rerun()