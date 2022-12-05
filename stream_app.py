import datetime
from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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



st.title('Trip to Madrid')
csv_csv = pd.read_csv('csv_csv.csv')

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


cols = st.columns((2, 1, .5))
mylist = csv_csv['title']+" ("+csv_csv['status']+") "
place = cols[0].selectbox("Status", options=list(mylist))
sts = cols[1].selectbox("Status", options=("Done", "ToDo"))

if cols[2].button("Update"):
    csv_csv.loc[csv_csv["title"].str.contains(place[:-7]), "status"] = "Done"    
    csv_csv.to_csv('csv_csv.csv')
    cols[2].markdown("Saved!")
    st.write(place)
    st.write(place[:-7])
    st.write(sts)
    st.write(csv_csv.loc[(csv_csv["title"] == place[:-7])])


fig = plot_figure(csv_csv)
st.plotly_chart(fig, use_container_width=True)