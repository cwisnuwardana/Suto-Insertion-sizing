import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

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

st.image("suto_logo.png", width=460)
st.title("SUTO Flowmeter Installation Calculator")

st.write("SUTO Flowmeter Installation Tool")

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

    # =====================================================
    # PDF GENERATOR
    # =====================================================

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

        from reportlab.platypus import Image as RLImage
        from reportlab.platypus import Table
        from reportlab.platypus import TableStyle
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.styles import ParagraphStyle

        # =================================================
        # LOGO
        # =================================================

        try:
            logo = RLImage("suto_logo.png")
            logo.drawHeight = 60
            logo.drawWidth = 260
            elements.append(logo)
        except:
            pass

        elements.append(Spacer(1, 20))

        # =================================================
        # TITLE
        # =================================================

        title_style = ParagraphStyle(
            'title_style',
            parent=styles['Heading1'],
            alignment=TA_CENTER,
            textColor=colors.HexColor('#00A651'),
            fontSize=22,
            leading=28
        )

        title = Paragraph(
            "SUTO Flowmeter Installation Report",
            title_style
        )

        elements.append(title)
        elements.append(Spacer(1, 25))

        # =================================================
        # TABLE DATA
        # =================================================

        table_data = [
            ["Parameter", "Value"],
            ["Customer", customer],
            ["Flowmeter Type", flowmeter],
            ["Pipe Size", pipe_size],
            ["Pipe Schedule", pipe_schedule],
            ["Installation Condition", installation_condition],
            ["Installation Mode", installation_mode],
            ["Outer Diameter (OD)", f"{od:.2f} mm"],
            ["Wall Thickness (WT)", f"{wt:.2f} mm"],
            ["Inner Diameter (ID)", f"{id_mm:.2f} mm"],
            ["Insertion Depth", f"{insertion_depth:.2f} mm"],
            ["Upstream Distance", f"{upstream_mm:.2f} mm ({upstream_D}D)"],
            ["Downstream Distance", f"{downstream_mm:.2f} mm ({downstream_D}D)"],
            ["Point-to-Point Distance", f"{point_to_point_mm:.2f} mm ({total_D}D)"]
        ]

        table = Table(
            table_data,
            colWidths=[220, 250]
        )

        table.setStyle(TableStyle([

            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00A651')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),

            ('GRID', (0, 0), (-1, -1), 1, colors.grey),

            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),

            ('FONTSIZE', (0, 1), (-1, -1), 11),

            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
                colors.whitesmoke,
                colors.HexColor('#F4FFF8')
            ]),

            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10)
        ]))

        elements.append(table)

        elements.append(Spacer(1, 30))

        # =================================================
        # FOOTER NOTE
        # =================================================

        footer = Paragraph(
            "<i>This report is automatically generated by the SUTO Flowmeter Installation Calculator.</i>",
            styles['Italic']
        )

        elements.append(footer)

        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()

        return pdf

    pdf_file = generate_pdf()

    st.download_button(
        label="Download PDF Report",
        data=pdf_file,
        file_name="suto_installation_report.pdf",
        mime="application/pdf"
    )
