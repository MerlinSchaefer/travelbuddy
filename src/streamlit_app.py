import os

import folium
import geopandas as gpd
import streamlit as st
from dotenv import load_dotenv
from streamlit_folium import folium_static

# from prompts import ..
# from llm import load_base_LLM, load_chat_LLM

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="TravelBuddy", page_icon=":island:")

st.title("TravelBuddy")

# Load world map data
world_map = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))


# Sidebar for user input
st.sidebar.header("Select Continent and Country")
selected_continent = st.sidebar.selectbox(
    "Select a Continent", world_map["continent"].unique()
)
selected_country = (
    st.sidebar.selectbox(  # TODO enable overwrite before prompt submission
        "Select a Country",
        world_map[world_map["continent"] == selected_continent]["name"].tolist(),
    )
)
st.sidebar.header("Select travel modalities")
selected_local_type = st.sidebar.selectbox(
    "Select a local type",
    ["Nature", "City", "Both"],
)
selected_travel_type = st.sidebar.selectbox(
    "Select a travel type",
    ["Roundtrip", "Local Base", "Either"],
)
selected_transport_type = st.sidebar.selectbox(
    "Select a main transportation type",
    ["Train", "Plane and Car", "Plane, Walking and public transport", "Ship"],
)


# Color the selected country on the map
selected_country_geometry = world_map[world_map["name"] == selected_country][
    "geometry"
].values[0]
selected_country_center = selected_country_geometry.centroid
selected_country_lat, selected_country_lon = (
    selected_country_center.y,
    selected_country_center.x,
)

highlighted_map = folium.Map(
    location=[selected_country_lat, selected_country_lon], zoom_start=3
)  # Adjust zoom level here
folium.GeoJson(
    selected_country_geometry, style_function=lambda x: {"fillColor": "blue"}
).add_to(highlighted_map)
st.subheader(f"{selected_country} in {selected_continent}")
folium_static(highlighted_map)
