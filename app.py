## IMPORT LIBS
from streamlit.components.v1 import html
import tspmodel
import streamlit as st
from models import Routes
import readdata as rdt
from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *
from sqlalchemy.orm import sessionmaker
from models import Testing

@st.cache(allow_output_mutation=True)
def read_my_data():
    engine = create_engine('bigquery://third-light-372823', credentials_path='BIGQUERY_CREDENTIAL.json')
    Session = sessionmaker(bind=engine)
    session = Session()
    routes = Table('travelOptimization.testing', MetaData(bind=engine), autoload=True)
    sql_query = session.query(
    routes.c.ADDRESS_ID,
    routes.c.INDIVIDUAL_ID,
    routes.c.FIRST_NAME,
    routes.c.LAST_NAME    
    )
    routename = sql_query.all()
    return routename, session, routes

routename, session, routes=   read_my_data()  
st.table(routename)

ADDRESS_ID = (st.text_input('ADDRESS_ID').strip())
INDIVIDUAL_ID = (st.text_input('INDIVIDUAL_ID').strip())
FIRST_NAME = (st.text_input('FIRST_NAME').strip())
LAST_NAME = (st.text_input('LAST_NAME').strip())
try:
    st.write(ADDRESS_ID)
    st.write(INDIVIDUAL_ID)
    st.write(FIRST_NAME)
    st.write(LAST_NAME)
except:
    pass

st.write('Save route in filters')
if st.session_state.get('button') !=  True:
    st.session_state['button'] = st.button('Save')

# if button is clicked with routename chosen
if (st.session_state['button'] ==  True):
    exists = session.query(routes).filter_by(ADDRESS_ID=ADDRESS_ID[0]).first()

    if exists:
        st.write("this register already exists")
    else:
        testing = Testing(
            ADDRESS_ID = ADDRESS_ID,
            INDIVIDUAL_ID = INDIVIDUAL_ID,
            FIRST_NAME = FIRST_NAME,
            LAST_NAME = LAST_NAME,
        )
        session.add(testing)
        session.commit()
    st.write("Done")
