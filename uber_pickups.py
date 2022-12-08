import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Done! (using st.cache)')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')

hist_values=np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

#hour_to_filter = st.slider('hour', 0, 23, 17)
hour_to_filter = st.number_input('Enter Hour', min_value=0, max_value=23, step=1)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.metric(label='Hour Selected', value=hour_to_filter)
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
#st.map(filtered_data)

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=40.8,
        longitude=-74,
        zoom=10,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=filtered_data,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=filtered_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))








#hour_to_filter = st.slider('hour', 0, 23, 17)
#filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
#st.metric(label='Hour Selected', value=f"{abs(hour_to_filter - 12)} O'clock")
#st.subheader(f'Map of all pickups at {hour_to_filter}:00')
#st.map(filtered_data)