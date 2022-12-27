"""
    Explain
"""

## IMPORT LIBS
# from models import Routes
# from streamlit.components.v1 import html
import folium
import readdata as rdt
import streamlit as st
import tspmodel
from webbrowser import open

## PAGE LAYOUT
# Define the size of this page
st.set_page_config(layout = 'wide')

# config streamlit layout
hide_streamlit_style = \
    """
    <style>
        .css-18e3th9 {padding: 1.5rem 1rem 1rem;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html = True)

## TODO: Function to filter usersid
usersid = 1

## READ DATA
# TODO: df_original_tuple = rdt.read_df_original(usersid_filtered = usersid)
# TODO: routename = rdt.read_routename(usersid_filtered = usersid)

#######   TEMP   ####### 
import pandas as pd #THIS IS A TEMP SOLUTION
places = pd.read_csv("data/places.csv",index_col=[0]) #THIS IS A TEMP SOLUTION
comments = pd.read_csv("data/comments.csv",index_col=[0]) #THIS IS A TEMP SOLUTION
comments = comments[comments['usersid']==usersid] #THIS IS A TEMP SOLUTION
df = pd.merge(places,comments,how='left',left_on='id',right_on='placesid') #THIS IS A TEMP SOLUTION
df = df[df['city']=='barcelona'] #THIS IS A TEMP SOLUTION
df = df[['id','placename','lat','lng','routestatus']] #THIS IS A TEMP SOLUTION
df['routestatus'] =  df['routestatus'].fillna('ToDo') #THIS IS A TEMP SOLUTION
df_original_tuple = list(df.itertuples(index=False)) #THIS IS A TEMP SOLUTION
route = pd.read_csv("data/routes.csv",index_col=[0]) #THIS IS A TEMP SOLUTION
routename_all = list(route.itertuples(index=False))  #THIS IS A TEMP SOLUTION
routes = route[route['usersid']==usersid]  #THIS IS A TEMP SOLUTION
routename = list(routes.itertuples(index=False))  #THIS IS A TEMP SOLUTION
#######   TEMP   #######


## SECOND PART - FILTERS

# custom cols
custom_col1 = st.columns((1, 1))

# add the option all
filter_names = list(set([item[0] for item in routename])) # get unique filters
filter_names = sorted(filter_names)  # ordering alphabetically
filter_names.insert(0, 'All') # insert option all

# choose filter route options
route_filter = custom_col1[0].selectbox('Choose a filter', options = filter_names)

# If filter is All it remains as the original
if route_filter ==  'All':
    df_entrada_tuple = df_original_tuple.copy()

else:
    ## based on the name of the filter it will get the locations
    # find filter chosen by user
    chosen_filter = [item for item in routename if item[0] ==  route_filter]
    # list of places in that filter
    chosen_filter = [item[2] for item in chosen_filter]
    # list of tuples filtered by list of places in that filter
    df_entrada_tuple = [tuple for tuple in df_original_tuple if tuple[0] in chosen_filter]

# radio box to select back all places
radio = st.sidebar.radio('Select places to visit', ('All places for this filter', 'Places to be visited'))

# select name of all places available in database
all_original_places = [item[1] for item in df_original_tuple]

# show expander
my_expander = st.sidebar.expander(label = 'Advanced Filters')
with my_expander:
    # Select all from this filter
    if radio ==  'All places for this filter':
        to_visit = st.multiselect(
            'Select one or more options:',
            options = all_original_places,
            default = [item[1] for item in df_entrada_tuple])
    
    # in case select Remove places already visited 
    else:
        done = [item for item in df_entrada_tuple if item[4] !=  'Done']
        to_visit = st.multiselect(
            'Select one or more options:',
            options = all_original_places,
            default = [item[1] for item in done])

    if to_visit:
        df_entrada_tuple = [tuple for tuple in df_original_tuple if tuple[1] in to_visit]


# custom cols
custom_cols = st.sidebar.columns((1, 1))

# insert name of the route
routename_chosen = custom_cols[0].text_input('Name of Route').strip()

# this only set the button
custom_cols[1].write('Save route in filters')
if st.session_state.get('button') !=  True:
    st.session_state['button'] = custom_cols[1].button('Save')

# if button is clicked with routename chosen
if ((st.session_state['button'] ==  True) and (routename_chosen) and (routename_chosen!= 'All')):
    # TODO: exists = rdt.check_route_table(my_table = 'routes',routename_chosen = routename_chosen,usersid_filtered = usersid)
    exists = [item for item in routename if ((item[0]==routename_chosen)&(item[1]==usersid))] #THIS IS A TEMP SOLUTION
    placesid = [item[0] for item in df_entrada_tuple]
    iteraction = len(placesid)
    final_routename = [item for item in routename_all if ((item[0]!=routename_chosen)or(item[1]!=usersid))] #THIS IS A TEMP SOLUTION

    if exists:
        st.sidebar.write('This register already exists, what you wanna do?')
        custom_cols = st.sidebar.columns((1, 1))

        if custom_cols[0].button('Replace?'):
            ## first it deletes the filter for this user
            # TODO: rdt.delete_table(my_table = 'routes',routename_chosen = routename_chosen,usersid_filtered = usersid)
            ## apply changes
            # TODO: rdt.session.commit()
            # TODO: rdt.insert_table(
            #     iteraction = len(placesid),
            #     modeltable = Routes,
            #     routename_chosen = routename_chosen,
            #     usersid_filtered = usersid,
            #     placesid = placesid)
            for i in range(iteraction): #THIS IS A TEMP SOLUTION
                final_routename.append((routename_chosen,usersid,placesid[i])) #THIS IS A TEMP SOLUTION
            pd.DataFrame(final_routename).to_csv('data/routes.csv') #THIS IS A TEMP SOLUTION
            ## apply changes    
            # TODO: rdt.session.commit()
            st.sidebar.write('Done')
        
        # This will remove this filter
        if custom_cols[1].button('Delete?'):
            # TODO: rdt.delete_table(my_table = 'routes',routename_chosen = routename_chosen,usersid_filtered = usersid)
            ## apply changes  
            # TODO: rdt.session.commit()
            pd.DataFrame(final_routename).to_csv('data/routes.csv') #THIS IS A TEMP SOLUTION
            st.sidebar.write('Done')

    else:
        ## This will add a brand new record
        # TODO: rdt.insert_table(
        #     iteraction = len(placesid),
        #     modeltable = Routes,
        #     routename_chosen = routename_chosen,
        #     usersid_filtered = usersid,
        #     placesid = placesid)
        ## apply changes  
        # TODO: rdt.session.commit()
        # st.sidebar.write('Done')
        
        for i in range(iteraction): #THIS IS A TEMP SOLUTION
            routename_all.append((routename_chosen,usersid,placesid[i])) #THIS IS A TEMP SOLUTION
            pd.DataFrame(routename_all).to_csv('data/routes.csv') #THIS IS A TEMP SOLUTION
            st.sidebar.write('Done')

## third part - map the solution
# coordinates
coordinates = {tup[1]: (tup[2],tup[3]) for tup in df_entrada_tuple}

# myplaces
myplaces = [item[1] for item in df_entrada_tuple]

if len(myplaces) > 3:
    myplaces, coordinates = tspmodel.model_TSP(coordinates, myplaces)

# create points in map - All points - black
lat = [item[2] for item in df_original_tuple]
lng = [item[3] for item in df_original_tuple]
all_ = [tuple(x) for x in zip(lat, lng, all_original_places)] #tuple of coord

# create points in map - already visited - red  
done = [item for item in df_original_tuple if item[4] ==  'Done']
lat = [item[2] for item in done]
lng = [item[3] for item in done]
done = [tuple(x) for x in zip(lat, lng)] #tuple of coord

# create points in map - to be visited - green
todo = [item for item in df_entrada_tuple if item[4] !=  'Done']
lat  = [item[2] for item in todo]
lng  = [item[3] for item in todo]
todo = [tuple(x) for x in zip(lat, lng)] #tuple of coord

# create map
mappy = rdt.plotmap(todo=todo,done=done,allz=all_,myplaces=myplaces,coordinates=coordinates)

# create boundaries to centralize
latz = [item[2] for item in df_entrada_tuple]
lngz = [item[3] for item in df_entrada_tuple]
boundaries = [[min(latz),min(lngz)],[max(latz),max(lngz)]]

# fit mappy in these boundaries
mappy.fit_bounds(boundaries)

# plot map
st.write(mappy)

points = [] #THIS IS A TEMP SOLUTION
for city in myplaces: #THIS IS A TEMP SOLUTION
    points.append(coordinates[city]) #THIS IS A TEMP SOLUTION
points.append(points[0]) #THIS IS A TEMP SOLUTION



Z=[] #THIS IS A TEMP SOLUTION
for i in range(len(points)): #THIS IS A TEMP SOLUTION
    Z.append(','.join(map(str, points[i]))) #THIS IS A TEMP SOLUTION

custom_col1[1].write("Open on GoogleMaps")
if custom_col1[1].button('GoogleMaps'):
    if len(Z) > 25:
        custom_col1[1].warning(f"Sorry, GoogleMaps accepts up to 24 places. You have selected {len(Z)-1}")
    else:
        url = ("https://www.google.com/maps/dir/"+'/'.join(map(str, Z))+"/data=!3m1!4b1!4m2!4m1!3e2") #THIS IS A TEMP SOLUTION
        # webbrowser.open_new_tab(url)
        open(url)

# url = "https://www.google.com/maps/dir/41.403423,2.174611/41.41142,2.174328/41.391712,2.164824/41.39493,2.16177/41.395325,2.161925/41.39621,2.161339/41.40341,2.15066/41.412766,2.131519/41.4215,2.1192/41.380924,2.122952/41.37494,2.14834/41.371174,2.151718/41.368454,2.153715/41.36852,2.159726/41.364548,2.165427/41.378883,2.17424/41.38174,2.171584/41.382168,2.172549/41.387573,2.175302/41.387,2.17611/41.38442,2.17601/41.3827,2.177113/41.38349,2.18178/41.388542,2.18718/41.403423,2.174611/@41.3927926,2.113914,13z/data=!3m1!4b1!4m2!4m1!3e2"
