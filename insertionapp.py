import streamlit as st
from PIL import Image

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SUTO S401 Installation Calculator",
    layout="wide"
)

# =========================================================
# DATABASE
# =========================================================

pipe_database = {

    "2 inch (DN50)": {
        "od": 60.3,
        "schedules": {
            "SCH40": {
                "wt": 3.91
            },
            "SCH80": {
                "wt": 5.54
            }
        }
    },

    "3 inch (DN80)": {
        "od": 88.9,
        "schedules": {
            "SCH40": {
                "wt": 5.49
            }
        }
    }
}

installation_rules = {

    "90° Elbow": {
        "upstream_D": 20,
        "downstream_D": 5
    },

    "Valve": {
        "upstream_D": 50,
        "downstream_D": 5
    },

    "Tee": {
        "upstream_D": 25,
        "downstream_D": 5
    }
}

# =========================================================
# HEADER
# =========================================================

st.title("SUTO S401 Installation Calculator")
st.subheader("Thermal Mass Flow Meter (Insertion)")

st.divider()

# =========================================================
# LAYOUT
# =========================================================

left_col, right_col = st.columns([1, 2])

# =========================================================
# LEFT SIDE INPUT
# =========================================================

with left_col:

    st.header("INPUT DATA")

    customer = st.text_input(
        "Customer",
        value="PT. ABC Pneumatic"
    )

    flowmeter = st.selectbox(
        "Flowmeter Type",
        [
            "S401-S",
            "S401-M",
            "S401-H"
        ]
    )

    condition = st.selectbox(
        "Installation Condition",
        [
            "90° Elbow",
            "Valve",
            "Tee"
        ]
    )

    pipe_size = st.selectbox(
        "Pipe Size",
        list(pipe_database.keys())
    )

    schedule = st.selectbox(
        "Pipe Schedule",
        [
            "SCH40",
            "SCH80"
        ]
    )

    valve_height = st.number_input(
        "Height of Valve (mm)",
        value=87.0
    )

    calculate = st.button(
        "GENERATE INSTALLATION",
        use_container_width=True
    )

# =========================================================
# CALCULATION
# =========================================================

pipe_data = pipe_database[pipe_size]

od = pipe_data["od"]

wt = pipe_data["schedules"][schedule]["wt"]

inner_diameter = od - (2 * wt)

insertion_depth = (od / 2) + valve_height

upstream_D = installation_rules[condition]["upstream_D"]

downstream_D = installation_rules[condition]["downstream_D"]

upstream_distance = inner_diameter * upstream_D

downstream_distance = inner_diameter * downstream_D

point_to_point = upstream_distance + downstream_distance

# =========================================================
# INSTALLATION MODE
# =========================================================

if inner_diameter > 200:
    installation_mode = "100 mm OFF-CENTER"
else:
    installation_mode = "CENTER INSTALLATION"

# =========================================================
# RIGHT SIDE OUTPUT
# =========================================================

with right_col:

    st.header("OUTPUT - INSTALLATION SUMMARY")

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Insertion Depth",
        f"{insertion_depth:.2f} mm"
    )

    metric2.metric(
        "Upstream Distance",
        f"{upstream_distance:.2f} mm"
    )

    metric3.metric(
        "Downstream Distance",
        f"{downstream_distance:.2f} mm"
    )

    st.divider()

    # =====================================================
    # INSTALLATION RESULT TABLE
    # =====================================================

    st.subheader("Calculation Result")

    st.write(f"**Customer:** {customer}")

    st.write(f"**Flowmeter:** {flowmeter}")

    st.write(f"**Pipe Size:** {pipe_size}")

    st.write(f"**Pipe Schedule:** {schedule}")

    st.write(f"**Installation Condition:** {condition}")

    st.write(f"**Installation Mode:** {installation_mode}")

    st.divider()

    st.write(f"### Pipe Information")

    st.write(f"Outer Diameter (OD): **{od:.2f} mm**")

    st.write(f"Wall Thickness (WT): **{wt:.2f} mm**")

    st.write(f"Inner Diameter (ID): **{inner_diameter:.2f} mm**")

    st.divider()

    st.write(f"### Installation Distance")

    st.write(f"Upstream Distance: **{upstream_distance:.2f} mm**")

    st.write(f"Downstream Distance: **{downstream_distance:.2f} mm**")

    st.write(f"Point-to-Point Distance: **{point_to_point:.2f} mm**")

    st.divider()

    # =====================================================
    # IMAGE
    # =====================================================

    st.subheader("Installation Diagram")

    image = Image.open("s401_installation.png")

    st.image(
        image,
        use_container_width=True
    )

    st.success(
        f"Minimum Point-to-Point Distance Required = {point_to_point:.2f} mm"
    )
