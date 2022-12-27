"""
    Explain
"""

## import libs
# from sqlalchemy import MetaData, func
# from models import Base, User, Routes, Places
# from database import session
import streamlit as st
import folium

#########
## read data: places and comments
@st.cache(allow_output_mutation=True)
def read_df_original(usersid_filtered=None):
    """TODO: Explains Later"""
    # tables that would be used
    places = Base.metadata.tables['places']
    comments = Base.metadata.tables['comments']

    # create sql
    sql_query = session.query(
        places.c.id,
        places.c.placename,
        places.c.lat,
        places.c.lng,
        func.coalesce(comments.c.routestatus, 'ToDo'),
    ).join(comments, comments.c.placesid == places.c.id and comments.c.usersid=={usersid_filtered} , isouter=True)

    # apply sql
    df_original_tuple = sql_query.all()
    return df_original_tuple

#########
## read data: routes
def read_routename(usersid_filtered=None):
    """TODO: Explains Later"""
    # tables that would be used
    routes = Base.metadata.tables['routes']
    # create sql
    sql_query = session.query(
        routes.c.routename,
        routes.c.usersid,
        routes.c.placesid
    ).filter_by(usersid=usersid_filtered)
    # apply sql
    routename = sql_query.all()
    return routename

#########
def filter_route_table(my_table=None,routename_chosen=None,usersid_filtered=None):
    """TODO: Explains Later"""
    my_table = Base.metadata.tables[my_table]
    return session.query(my_table).filter_by(routename=routename_chosen, usersid=usersid_filtered)

def check_route_table(my_table=None,routename_chosen=None,usersid_filtered=None):
    """TODO: Explains Later"""
    return filter_route_table(my_table=my_table,routename_chosen=routename_chosen,usersid_filtered=usersid_filtered).first()

## read data: routes
def delete_table(my_table=None,routename_chosen=None,usersid_filtered=None):
    """TODO: Explains Later"""
    filter_route_table(my_table=my_table,routename_chosen=routename_chosen,usersid_filtered=usersid_filtered).delete()

def insert_table(iteraction=None,modeltable=None,routename_chosen=None,usersid_filtered=None,placesid=None):
    """TODO: Explains Later"""
    # Now it adds the filter chosen
    for i in range(iteraction):
        routes = Routes(
            routename = routename_chosen,
            usersid = usersid_filtered,
            placesid = placesid[i],
        )
        session.add(routes)


@st.cache(allow_output_mutation = True)
def plotmap(todo=None,done=None,allT=None,myplaces=None,coordinates=None):
    """TODO: Explains Later"""
    # filter coord
    points = []
    for city in myplaces:
        points.append(coordinates[city])
    points.append(points[0])

    # create map
    mappy = folium.Map()
    # folium.TileLayer('stamenterrain').add_to(mappy)
    # folium.TileLayer('openstreetmap').add_to(mappy)
    # folium.TileLayer('stamentoner').add_to(mappy)
    # folium.TileLayer('cartodbpositron').add_to(mappy)

    # add Layer Control
    # folium.LayerControl().add_to(mappy)

    # create lines between poins
    folium.PolyLine(points, color = "green", opacity = 1).add_to(mappy)

    # create points in map - to be visited
    # for lats, lons in todo:
    #     mappy.add_child(folium.CircleMarker(
    #         location = [lats, lons],
    #         radius = 7,
    #         color = "green",
    #         fill = True,
    #         fill_opacity = 1))

    # create points in map - already visited   
    # for lats, lons in done:
    #     mappy.add_child(folium.CircleMarker(
    #         location = [lats, lons],
    #         radius = 7,
    #         color = "red",
    #         fill = True,
    #         fill_opacity = 1))
    
    # create points in map - all places
    for lats, lons, title in allT:
        # Define html inside marker pop-up
        # column_html = folium.Html(f"""
        # <p style = "text-align: center;">{title}</p>
        # """, script = True)
        # popup = folium.Popup(column_html)
        mappy.add_child(folium.CircleMarker(
            location = [lats, lons],
            radius = 4,
            # popup = popup,
            color = "black",
            fill = True,
            # tooltip = f'{title}',
            fill_opacity = 1))

    return (mappy)