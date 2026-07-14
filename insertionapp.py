import streamlit as st
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage
)
from suto_footer import (show_suto_footer)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle

from io import BytesIO

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SUTO Flowmeter Installation Calculator",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f6f7;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.metric-card {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #dfe6e9;
}

.green-text {
    color: #00A651;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PIPE DATABASE ANSI B36.10 / B36.19
# =========================================================

pipe_database = {

    '1"': {
        "dn": 25,
        "od": 33.4,
        "schedules": {
            "SCH10": 2.77,
            "SCH40": 3.38,
            "SCH80": 4.55,
            "SCH160": 6.35
        }
    },

    '1.5"': {
        "dn": 40,
        "od": 48.3,
        "schedules": {
            "SCH10": 2.77,
            "SCH40": 3.68,
            "SCH80": 5.08,
            "SCH160": 7.14
        }
    },

    '2"': {
        "dn": 50,
        "od": 60.3,
        "schedules": {
            "SCH10": 2.77,
            "SCH40": 3.91,
            "SCH80": 5.54,
            "SCH160": 8.74
        }
    },

    '2.5"': {
        "dn": 65,
        "od": 73.0,
        "schedules": {
            "SCH10": 3.05,
            "SCH40": 5.16,
            "SCH80": 7.01,
            "SCH160": 9.53
        }
    },

    '3"': {
        "dn": 80,
        "od": 88.9,
        "schedules": {
            "SCH10": 3.05,
            "SCH40": 5.49,
            "SCH80": 7.62,
            "SCH160": 11.13
        }
    },

    '4"': {
        "dn": 100,
        "od": 114.3,
        "schedules": {
            "SCH10": 3.05,
            "SCH40": 6.02,
            "SCH80": 8.56,
            "SCH160": 13.49
        }
    },

    '5"': {
        "dn": 125,
        "od": 141.3,
        "schedules": {
            "SCH10": 3.40,
            "SCH40": 6.55,
            "SCH80": 9.53,
            "SCH160": 15.88
        }
    },

    '6"': {
        "dn": 150,
        "od": 168.3,
        "schedules": {
            "SCH10": 3.40,
            "SCH40": 7.11,
            "SCH80": 10.97,
            "SCH160": 18.26
        }
    },

    '8"': {
        "dn": 200,
        "od": 219.1,
        "schedules": {
            "SCH10": 3.76,
            "SCH40": 8.18,
            "SCH80": 12.70,
            "SCH160": 18.26
        }
    },

    '10"': {
        "dn": 250,
        "od": 273.1,
        "schedules": {
            "SCH10": 4.19,
            "SCH40": 9.27,
            "SCH80": 12.70,
            "SCH160": 21.44
        }
    },

    '12"': {
        "dn": 300,
        "od": 323.9,
        "schedules": {
            "SCH10": 4.57,
            "SCH40": 9.53,
            "SCH80": 12.70,
            "SCH160": 25.40
        }
    }
}

# =========================================================
# INSTALLATION RULES
# =========================================================

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

# =========================================================
# HEADER
# =========================================================

try:
    st.image("suto_logo.png", width=320)
except:
    pass

st.title("SUTO Flowmeter Installation Calculator")

st.write("Thermal Mass Flowmeter Installation Tool")

st.divider()

# =========================================================
# MAIN LAYOUT
# =========================================================

left_col, right_col = st.columns([1, 2])

# =========================================================
# LEFT INPUT
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

    available_schedules = list(
        pipe_database[pipe_size]["schedules"].keys()
    )

    pipe_schedule = st.selectbox(
        "Pipe Schedule",
        available_schedules
    )

    installation_condition = st.selectbox(
        "Installation Condition",
        list(installation_rules.keys())
    )

    valve_height = st.number_input(
        "Ball Valve Height (mm)",
        value=70.0
    )

    napple_height = st.number_input(
        "Napple Height (mm)",
        value=20.0
    )

# =========================================================
# CALCULATION
# =========================================================

pipe_data = pipe_database[pipe_size]

od = pipe_data["od"]

wt = pipe_data["schedules"][pipe_schedule]

id_mm = od - (2 * wt)

pipe_radius = od / 2

insertion_depth = (
    valve_height +
    napple_height +
    pipe_radius
)

upstream_D = installation_rules[
    installation_condition
]["upstream_D"]

downstream_D = installation_rules[
    installation_condition
]["downstream_D"]

upstream_mm = dn * upstream_D

downstream_mm = dn * downstream_D

point_to_point_mm = (
    upstream_mm +
    downstream_mm
)

total_D = (
    upstream_D +
    downstream_D
)

cross_section_area = (
    3.14159 *
    ((id_mm / 2) ** 2)
) / 100

# =========================================================
# INSTALLATION MODE
# =========================================================

if id_mm > 200:
    installation_mode = "100 mm OFF-CENTER"
else:
    installation_mode = "CENTER INSTALLATION"

# =========================================================
# RIGHT OUTPUT
# =========================================================

with right_col:

    st.header("OUTPUT SUMMARY")

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Insertion Depth",
        f"{insertion_depth:.2f} mm"
    )

    metric2.metric(
        "Upstream",
        f"{upstream_mm:.2f} mm"
    )

    metric3.metric(
        "Downstream",
        f"{downstream_mm:.2f} mm"
    )

    st.divider()

    st.subheader("Calculation Result")

    st.write(
        f"**Customer:** {customer}"
    )

    st.write(
        f"**Flowmeter Type:** {flowmeter}"
    )

    st.write(
        f"**Pipe Size:** {pipe_size}"
    )

    st.write(
        f"**Pipe Schedule:** {pipe_schedule}"
    )

    st.write(
        f"**Installation Condition:** "
        f"{installation_condition}"
    )

    st.write(
        f"**Installation Mode:** "
        f"{installation_mode}"
    )

    st.divider()

    st.subheader(
        "Pipe Dimension"
    )

    st.write(
        f"Outside Diameter (OD): "
        f"{od:.2f} mm"
    )

    st.write(
        f"Wall Thickness (WT): "
        f"{wt:.2f} mm"
    )

    st.write(
        f"Inner Diameter (ID): "
        f"{id_mm:.2f} mm"
    )

    st.write(
        f"Cross Section Area: "
        f"{cross_section_area:.2f} cm²"
    )

    st.divider()

    st.subheader(
        "Installation Stack-up"
    )

    st.write(
        f"Ball Valve Height: "
        f"{valve_height:.2f} mm"
    )

    st.write(
        f"Napple Height: "
        f"{napple_height:.2f} mm"
    )

    st.write(
        f"Pipe Radius: "
        f"{pipe_radius:.2f} mm"
    )

    st.write(
        f"Installation Depth: "
        f"{insertion_depth:.2f} mm"
    )

    st.divider()

    st.subheader(
        "Straight Pipe Requirement"
    )

    st.write(
        f"Upstream Distance: "
        f"{upstream_mm:.2f} mm "
        f"({upstream_D}D)"
    )

    st.write(
        f"Downstream Distance: "
        f"{downstream_mm:.2f} mm "
        f"({downstream_D}D)"
    )

    st.write(
        f"Point-to-Point Distance: "
        f"{point_to_point_mm:.2f} mm "
        f"({total_D}D)"
    )

# =========================================================
# PDF GENERATOR
# =========================================================

def generate_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    elements = []

    try:

        logo = RLImage(
            "suto_logo.png"
        )

        logo.drawHeight = 50
        logo.drawWidth = 220

        elements.append(logo)

    except:
        pass

    elements.append(Spacer(1, 20))

    title_style = ParagraphStyle(
        'title_style',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        textColor=colors.HexColor('#00A651'),
        fontSize=22
    )

    title = Paragraph(
        "SUTO Flowmeter Installation Report",
        title_style
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    table_data = [

        ["Parameter", "Value"],

        ["Customer", customer],

        ["Flowmeter Type", flowmeter],

        ["Pipe Size", pipe_size],

        ["Pipe Schedule", pipe_schedule],

        ["Installation Condition",
         installation_condition],

        ["Installation Mode",
         installation_mode],

        ["OD",
         f"{od:.2f} mm"],

        ["WT",
         f"{wt:.2f} mm"],

        ["ID",
         f"{id_mm:.2f} mm"],

        ["Cross Section Area",
         f"{cross_section_area:.2f} cm²"],

        ["Ball Valve Height",
         f"{valve_height:.2f} mm"],

        ["Napple Height",
         f"{napple_height:.2f} mm"],

        ["Installation Depth",
         f"{insertion_depth:.2f} mm"],

        ["Upstream Distance",
         f"{upstream_mm:.2f} mm ({upstream_D}D)"],

        ["Downstream Distance",
         f"{downstream_mm:.2f} mm ({downstream_D}D)"],

        ["Point-to-Point Distance",
         f"{point_to_point_mm:.2f} mm ({total_D}D)"]
    ]

    table = Table(
        table_data,
        colWidths=[220, 250]
    )

    table.setStyle(TableStyle([

        ('BACKGROUND',
         (0, 0),
         (-1, 0),
         colors.HexColor('#00A651')),

        ('TEXTCOLOR',
         (0, 0),
         (-1, 0),
         colors.white),

        ('FONTNAME',
         (0, 0),
         (-1, 0),
         'Helvetica-Bold'),

        ('FONTSIZE',
         (0, 0),
         (-1, 0),
         12),

        ('GRID',
         (0, 0),
         (-1, -1),
         1,
         colors.grey),

        ('ROWBACKGROUNDS',
         (0, 1),
         (-1, -1),
         [
             colors.whitesmoke,
             colors.HexColor('#F4FFF8')
         ])
    ]))

    elements.append(table)

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf

# =========================================================
# DOWNLOAD PDF
# =========================================================

pdf_file = generate_pdf()

st.download_button(
    label="Download PDF Report",
    data=pdf_file,
    file_name="suto_installation_report.pdf",
    mime="application/pdf"
)
show_suto_footer()
