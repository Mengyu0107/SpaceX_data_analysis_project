import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Load data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()


# Create Dash app
app = dash.Dash(__name__)


# App layout
app.layout = html.Div(children=[

    html.H1(
        "SpaceX Launch Records Dashboard",
        style={
            "textAlign": "center",
            "color": "#503D36",
            "font-size": 40
        }
    ),

    # Dropdown
    dcc.Dropdown(
        id="site-dropdown",
        options=[
            {"label": "All Sites", "value": "ALL"},
            {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
            {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
            {"label": "KSC LC-39A", "value": "KSC LC-39A"},
            {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"}
        ],
        value="ALL",
        placeholder="Select a Launch Site",
        searchable=True
    ),

    html.Br(),

    # Pie chart
    html.Div(
        dcc.Graph(id="success-pie-chart")
    ),

    html.Br(),

    # Payload slider
    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id="payload-slider",
        min=0,
        max=10000,
        step=1000,
        marks={
            0: "0",
            2500: "2500",
            5000: "5000",
           