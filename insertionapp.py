import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="SUTO Installation Calculator",
    layout="wide"
)

# =====================================================
# PIPE DATABASE
# =====================================================

pipe_database = {

    '1"': {"od": 33.4},
    '1.5"': {"od": 48.3},
    '2"': {"od": 60.3},
    '2.5"': {"od": 73.0},
    '3"': {"od": 88.9},
    '4"': {"od": 114.3},
    '5"': {"od": 141.3},
    '6"': {"od": 168.3},
    '8"': {"od": 219.1},
    '10"': {"od": 273.0},
    '12"': {"od": 323.8}
}

# =====================================================
# PIPE SCHEDULE DATABASE
# =====================================================

schedule_database = {

    "SCH10": 3.0,
    "SCH20": 4.0,
    "SCH40": 5.0,
    "SCH60": 6.0,
    "SCH80": 8.0,
    "SCH100": 10.0,
    "SCH120": 12.0,
    "SCH140": 14.0,
    "SCH160": 16.0
}

# =====================================================
# INSTALLATION RULES
# =====================================================

installation_rules = {

    "Expansion": {
        "upstream_D": 20,
        "downstream_D": 5
    },

    "Reduction": {
        "upstream_D": 20,
        "downstream_D": 5
    },

    "90° Bend": {
        "upstream_D": 20,
        "downstream_D": 5
    },

    "2 x 90° Bend": {
        "upstream_D": 25,
        "downstream_D": 5
    },

    "Three-dimensional Bend": {
        "upstream_D": 40,
        "downstream_D": 5
    },

    "T-piece": {
        "upstream_D": 25,
        "downstream_D": 5
    },

    "Shut-off Valve": {
        "upstream_D": 50,
        "downstream_D": 5
    },

    "Filter or Unknown Object": {
        "upstream_D": 50,
        "downstream_D": 5
    }
}

# =====================================================
# TITLE
# =====================================================

st.image("suto_logo.png", width=260)
st.title("SUTO Flowmeter Installation Calculator")

st.write("Thermal Mass Flowmeter Installation Tool")

st.divider()

# =====================================================
# LAYOUT
# =====================================================

left_col, right_col = st.columns([1, 2])

# =====================================================
# INPUT
# =====================================================

with left_col:

    st.header("INPUT DATA")

    customer = st.text_input(
        "Customer"
    )

    flowmeter = st.selectbox(
        "Flowmeter Type",
        [
            "S401-S",
            "S401-M",
            "S401-H",
            "S415",
            "S418-V",
            "S418-C",
            "S421",
            "S450",
            "S452"
        ]
    )

    pipe_size = st.selectbox(
        "Pipe Size",
        list(pipe_database.keys())
    )

    pipe_schedule = st.selectbox(
        "Pipe Schedule",
        list(schedule_database.keys())
    )

    installation_condition = st.selectbox(
        "Installation Condition",
        list(installation_rules.keys())
    )

    valve_height = st.number_input(
        "Valve Height (mm)",
        value=87.0
    )

# =====================================================
# CALCULATION
# =====================================================

od = pipe_database[pipe_size]["od"]

wt = schedule_database[pipe_schedule]

id_mm = od - (2 * wt)

insertion_depth = (od / 2) + valve_height

upstream_D = installation_rules[installation_condition]["upstream_D"]

downstream_D = installation_rules[installation_condition]["downstream_D"]

upstream_mm = id_mm * upstream_D

downstream_mm = id_mm * downstream_D

point_to_point_mm = upstream_mm + downstream_mm

total_D = upstream_D + downstream_D

# =====================================================
# INSTALLATION MODE
# =====================================================

if id_mm > 200:
    installation_mode = "100 mm OFF-CENTER"
else:
    installation_mode = "CENTER INSTALLATION"

# =====================================================
# OUTPUT
# =====================================================

with right_col:

    st.header("OUTPUT SUMMARY")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Insertion Depth",
        f"{insertion_depth:.2f} mm"
    )

    col2.metric(
        "Upstream",
        f"{upstream_mm:.2f} mm"
    )

    col3.metric(
        "Downstream",
        f"{downstream_mm:.2f} mm"
    )

    st.divider()

    st.subheader("Calculation Result")

    st.write(f"Customer: {customer}")

    st.write(f"Flowmeter Type: {flowmeter}")

    st.write(f"Pipe Size: {pipe_size}")

    st.write(f"Pipe Schedule: {pipe_schedule}")

    st.write(f"Installation Condition: {installation_condition}")

    st.write(f"Installation Mode: {installation_mode}")

    st.divider()

    st.write(f"Outer Diameter (OD): {od:.2f} mm")

    st.write(f"Wall Thickness (WT): {wt:.2f} mm")

    st.write(f"Inner Diameter (ID): {id_mm:.2f} mm")

    st.write(f"Insertion Depth: {insertion_depth:.2f} mm")

    st.divider()

    st.write(
        f"Upstream Distance: "
        f"{upstream_mm:.2f} mm ({upstream_D}D)"
    )

    st.write(
        f"Downstream Distance: "
        f"{downstream_mm:.2f} mm ({downstream_D}D)"
    )

    st.write(
        f"Point-to-Point Distance: "
        f"{point_to_point_mm:.2f} mm ({total_D}D)"
    )
