"""
    Explain
"""

## IMPORT LIBS
from streamlit.components.v1 import html
import tspmodel
import streamlit as st
from models import Routes
import readdata as rdt

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
df_original_tuple = rdt.read_df_original(usersid_filtered = usersid)
routename = rdt.read_routename(usersid_filtered = usersid)


## SECOND PART - FILTERS

# custom cols
custom_cols = st.columns((1, 1))

# add the option all
filter_names = list(set([item[0] for item in routename])) # get unique filters
filter_names = sorted(filter_names)  # ordering alphabetically
filter_names.insert(0, 'All') # insert option all

# choose filter route options
route_filter = custom_cols[0].selectbox('Choose a filter', options = filter_names)

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
    exists = rdt.check_route_table(my_table = 'routes',routename_chosen = routename_chosen,usersid_filtered = usersid)
    placesid = [item[0] for item in df_entrada_tuple]
    iteraction = len(placesid)
    
    if exists:
        st.sidebar.write('This register already exists, what you wanna do?')
        custom_cols = st.sidebar.columns((1, 1))

        if custom_cols[0].button('Replace?'):
            # first it deletes the filter for this user
            rdt.delete_table(my_table = 'routes',routename_chosen = routename_chosen,usersid_filtered = usersid)
            # apply changes
            rdt.session.commit()

            rdt.insert_table(
                iteraction = len(placesid),
                modeltable = Routes,
                routename_chosen = routename_chosen,
                usersid_filtered = usersid,
                placesid = placesid)

            # apply changes    
            rdt.session.commit()
            st.sidebar.write('Done')
        
        # This will remove this filter
        if custom_cols[1].button('Delete?'):
            rdt.delete_table(my_table = 'routes',routename_chosen = routename_chosen,usersid_filtered = usersid)
            # apply changes  
            rdt.session.commit()
            st.sidebar.write('Done')

    else:
        # This will add a brand new record
        rdt.insert_table(
            iteraction = len(placesid),
            modeltable = Routes,
            routename_chosen = routename_chosen,
            usersid_filtered = usersid,
            placesid = placesid)
        # apply changes  
        rdt.session.commit()
        st.sidebar.write('Done')


## third part - map the solution
# coordinates
coordinates = {tup[1]: (tup[2],tup[3]) for tup in df_entrada_tuple}

# myplaces
myplaces = [item[1] for item in df_entrada_tuple]

if len(myplaces) > 3:
    myplaces, coordinates = tspmodel.model_TSP(coordinates, myplaces)

# create points in map - All points
lat = [item[2] for item in df_original_tuple]
lng = [item[3] for item in df_original_tuple]
all_ = [tuple(x) for x in zip(lat, lng, all_original_places)] #tuple of coord

# create points in map - already visited   
done = [item for item in df_original_tuple if item[4] ==  'Done']
lat = [item[2] for item in done]
lng = [item[3] for item in done]
done = [tuple(x) for x in zip(lat, lng)] #tuple of coord

# create points in map - to be visited
todo = [item for item in df_entrada_tuple if item[4] !=  'Done']
lat = [item[2] for item in todo]
lng = [item[3] for item in todo]
todo = [tuple(x) for x in zip(lat, lng)] #tuple of coord

# create map
mappy = rdt.plotmap(todo=todo,done=done,all=all_,myplaces=myplaces,coordinates=coordinates)


asasasas=True
if asasasas:
    # create boundaries to centralize
    latz = [item[2] for item in df_entrada_tuple]
    lngz = [item[3] for item in df_entrada_tuple]
    boundaries = [[min(latz),min(lngz)],[max(latz),max(lngz)]]

    # fit mappy in these boundaries
    mappy.fit_bounds(boundaries)

else:
    mappy.fit_bounds(mappy.get_bounds(), padding=(30, 30))

# plot map
st.write(mappy)

## Fourth part - Save what is Done
# st.markdown("---")
# custom_col_2 = st.columns((2, 1, .5))
# mylist = df_original['title']+" (" + df_original['status']+") "
# place = custom_col_2[0].selectbox("Status", options = list(mylist))[:-8]
# sts = custom_col_2[1].selectbox("Status", options = ("Done", "ToDo"))

# custom_col_2[2].write("Save")
# if custom_col_2[2].button("Update"):
#     df_original.loc[df_original['title'].str.contains(
#         place, regex = False), "status"] = sts
#     df_original.to_csv(f'{city}.csv', index = [0])
#     custom_col_2[2].markdown("Saved!")

html("""
    <script language = "javascript">
    navigator.geolocation.getCurrentPosition(
        (loc)  = > {
            document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
        }
    )
    </script>
    """)
