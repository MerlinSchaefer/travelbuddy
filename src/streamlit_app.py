import os

import folium
import geopandas as gpd
import streamlit as st
from dotenv import load_dotenv
from langchain import ConversationChain
from streamlit_folium import folium_static

from llm import load_chat_LLM
from prompts import (apply_input_modifiers, create_initial_prompt_template,
                     prompt_input_modifiers, system_text_travel_agent,
                     user_text_travel_prompt)

# from prompts import ..
# from llm import load_base_LLM, load_chat_LLM

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# Load world map data
world_map = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Page setup
st.set_page_config(page_title="TravelBuddy", page_icon=":island:")
st.title("TravelBuddy")


### Sidebar for user input
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

###


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


# Create text input fields on the main page
st.write("Modify Values:")
destination = st.text_input("Selected Destination", selected_country)
duration = st.text_input("Selected Duration", "two weeks")
mode_of_exploration = st.text_input("Selected Local Type", selected_local_type)
mode_of_travel = st.text_input("Selected Travel Type", selected_travel_type)
mode_of_transport = st.text_input("Selected Transport Type", selected_transport_type)
additional_info = st.text_input("Additional Information")


# Create a "Submit" button
if st.button("Submit"):
    # Create text to submit to llm
    prompt_input = {
        "destination": destination,
        "duration": duration,
        "mode_of_transport": mode_of_transport,
        "mode_of_travel": mode_of_travel,
        "mode_of_exploration": mode_of_exploration,
        "additional_info": additional_info,
    }
    modified_input = apply_input_modifiers(prompt_input, prompt_input_modifiers)
    initial_prompt = create_initial_prompt_template(
        user_prompt_text=user_text_travel_prompt,
        system_prompt_text=system_text_travel_agent,
        input_data=modified_input,
    )
    st.write("## Travel Request")
    st.write(initial_prompt)
    # instantiate llm and conversation chain
    travel_chat = load_chat_LLM(openai_api_key=openai_api_key)
    conversation = ConversationChain(llm=travel_chat, verbose=True)
    st.write("## Travel Suggestion ")
    st.write(conversation.predict(input=initial_prompt))
