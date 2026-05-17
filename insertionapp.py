# ============================================================
# SUTO S401 INSTALLATION CALCULATOR
# PROFESSIONAL ENGINEERING GUI
# ============================================================

import streamlit as st 
from PIL import Image
import math

# ============================================================
# WINDOW SETUP
# ============================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("SUTO S401 Installation Calculator")
app.geometry("1600x900")

# ============================================================
# DATABASE
# ============================================================

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

# ============================================================
# MAIN LAYOUT
# ============================================================

left_frame = ctk.CTkFrame(app, width=420)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

right_frame = ctk.CTkFrame(app)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# ============================================================
# LEFT SIDE - INPUT
# ============================================================

title = ctk.CTkLabel(
    left_frame,
    text="INPUT DATA",
    font=("Arial", 24, "bold")
)
title.pack(pady=20)

# CUSTOMER

customer_label = ctk.CTkLabel(left_frame, text="Customer")
customer_label.pack(anchor="w", padx=20)

customer_entry = ctk.CTkEntry(left_frame, width=350)
customer_entry.pack(padx=20, pady=10)

# FLOWMETER

flowmeter_label = ctk.CTkLabel(left_frame, text="Flowmeter Type")
flowmeter_label.pack(anchor="w", padx=20)

flowmeter_option = ctk.CTkOptionMenu(
    left_frame,
    values=["S401-S", "S401-M", "S401-H"]
)
flowmeter_option.pack(padx=20, pady=10)

# INSTALLATION CONDITION

condition_label = ctk.CTkLabel(left_frame, text="Installation Condition")
condition_label.pack(anchor="w", padx=20)

condition_option = ctk.CTkOptionMenu(
    left_frame,
    values=[
        "90° Elbow",
        "Valve",
        "Tee"
    ]
)
condition_option.pack(padx=20, pady=10)

# PIPE SIZE

pipe_label = ctk.CTkLabel(left_frame, text="Pipe Size")
pipe_label.pack(anchor="w", padx=20)

pipe_option = ctk.CTkOptionMenu(
    left_frame,
    values=list(pipe_database.keys())
)
pipe_option.pack(padx=20, pady=10)

# PIPE SCHEDULE

schedule_label = ctk.CTkLabel(left_frame, text="Pipe Schedule")
schedule_label.pack(anchor="w", padx=20)

schedule_option = ctk.CTkOptionMenu(
    left_frame,
    values=["SCH40", "SCH80"]
)
schedule_option.pack(padx=20, pady=10)

# BALL VALVE HEIGHT

valve_label = ctk.CTkLabel(
    left_frame,
    text="Height of Valve (mm)"
)
valve_label.pack(anchor="w", padx=20)

valve_entry = ctk.CTkEntry(left_frame, width=350)
valve_entry.insert(0, "87")
valve_entry.pack(padx=20, pady=10)

# ============================================================
# OUTPUT LABELS
# ============================================================

result_title = ctk.CTkLabel(
    right_frame,
    text="OUTPUT - INSTALLATION SUMMARY",
    font=("Arial", 24, "bold")
)
result_title.pack(pady=20)

result_box = ctk.CTkTextbox(
    right_frame,
    width=500,
    height=250,
    font=("Consolas", 18)
)
result_box.pack(pady=20)

# ============================================================
# IMAGE PREVIEW
# ============================================================

image = ctk.CTkImage(
    light_image=Image.open("s401_installation.png"),
    size=(800, 500)
)

image_label = ctk.CTkLabel(
    right_frame,
    image=image,
    text=""
)

image_label.pack(pady=10)

# ============================================================
# CALCULATION FUNCTION
# ============================================================

def calculate():

    result_box.delete("1.0", "end")

    # GET INPUTS

    pipe_size = pipe_option.get()
    schedule = schedule_option.get()
    condition = condition_option.get()

    valve_height = float(valve_entry.get())

    # PIPE DATA

    od = pipe_database[pipe_size]["od"]

    wt = pipe_database[pipe_size]["schedules"][schedule]["wt"]

    # CALCULATE ID

    inner_diameter = od - (2 * wt)

    # INSTALLATION DEPTH

    insertion_depth = (od / 2) + valve_height

    # INSTALLATION RULES

    upstream_D = installation_rules[condition]["upstream_D"]

    downstream_D = installation_rules[condition]["downstream_D"]

    # DISTANCE

    upstream_distance = inner_diameter * upstream_D

    downstream_distance = inner_diameter * downstream_D

    total_distance = upstream_distance + downstream_distance

    # INSTALLATION MODE

    if inner_diameter > 200:
        installation_mode = "100 mm OFF-CENTER"
    else:
        installation_mode = "CENTER INSTALLATION"

    # OUTPUT

    output = f"""

CUSTOMER:
{customer_entry.get()}

====================================

FLOWMETER:
{flowmeter_option.get()}

PIPE SIZE:
{pipe_size}

PIPE SCHEDULE:
{schedule}

====================================

PIPE OUTER DIAMETER:
{od:.2f} mm

WALL THICKNESS:
{wt:.2f} mm

INNER DIAMETER:
{inner_diameter:.2f} mm

====================================

INSTALLATION MODE:
{installation_mode}

INSERTION DEPTH:
{insertion_depth:.2f} mm

====================================

UPSTREAM DISTANCE:
{upstream_distance:.2f} mm

DOWNSTREAM DISTANCE:
{downstream_distance:.2f} mm

POINT TO POINT DISTANCE:
{total_distance:.2f} mm

====================================

FLOW CONDITION:
{condition}

"""

    result_box.insert("1.0", output)

# ============================================================
# CALCULATE BUTTON
# ============================================================

calculate_button = ctk.CTkButton(
    left_frame,
    text="GENERATE INSTALLATION",
    command=calculate,
    height=50,
    font=("Arial", 18, "bold")
)

calculate_button.pack(pady=30)

# ============================================================
# RUN APP
# ============================================================

app.mainloop()
