
import streamlit as st
import os
import json
from PIL import Image


st.set_page_config(
    page_title="HydroFoundation Dashboard",
    layout="wide"
)

BASE = "assets"


st.title("🌊 HydroFoundation Dashboard")
st.write(
    "AI-based watershed digital twin visualization"
)


# Metadata
metadata_file = os.path.join(BASE,"metadata.json")

if os.path.exists(metadata_file):

    with open(metadata_file) as f:
        metadata = json.load(f)

    st.sidebar.write(metadata)



# Basin selector
basin = st.sidebar.number_input(
    "Select Basin",
    min_value=1,
    max_value=71,
    value=1
)


image_path = os.path.join(
    BASE,
    "basin_images",
    f"basin_{basin:03d}.png"
)


if os.path.exists(image_path):

    st.subheader(
        f"Basin {basin}"
    )

    img = Image.open(image_path)

    st.image(
        img,
        use_container_width=True
    )


# Figures

st.subheader("HydroFoundation Outputs")


figures = [
    "watershed_vulnerability_map.png",
    "attention_map.png",
    "basin_digital_twin.png",
    "basin_similarity_map.png"
]


for fig in figures:

    path = os.path.join(
        BASE,
        "figures",
        fig
    )

    if os.path.exists(path):

        st.image(
            path,
            caption=fig,
            use_container_width=True
        )
