# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()


# Create Dash app
app = dash.Dash(__name__)


# App layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "font-size": 40,
            },
        ),

        # TASK 1: Dropdown
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
                {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
            ],
            value="ALL",
            placeholder="Select a Launch Site",
            searchable=True,
        ),

        html.Br(),

        # TASK 2: Pie chart
        html.Div(
            dcc.Graph(id="success-pie-chart")
        ),

        html.Br(),

        html.P("Payload range (Kg):"),

        # TASK 3: Payload slider
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={
                0: "0",
                2500: "2500",
                5000: "5000",
                7500: "7500",
                10000: "10000",
            },
            value=[min_payload, max_payload],
        ),

        html.Br(),

        # TASK 4: Scatter chart
        html.Div(
            dcc.Graph(id="success-payload-scatter-chart")
        ),
    ]
)


# Callback for pie chart
@app.callback(
    Output(
        component_id="success-pie-chart",
        component_property="figure",
    ),
    Input(
        component_id="site-dropdown",
        component_property="value",
    ),
)
def get_pie_chart(selected_site):

    if selected_site == "ALL":

        # Only successful launches
        success_df = spacex_df[
            spacex_df["class"] == 1
        ]

        fig = px.pie(
            success_df,
            names="Launch Site",
            title="Total Success Launches by Site",
        )

        return fig

    else:

        # Only selected site
        site_df = spacex_df[
            spacex_df["Launch Site"] == selected_site
        ].copy()

        site_df["Outcome"] = site_df["class"].map(
            {
                1: "Success",
                0: "Failure",
            }
        )

        fig = px.pie(
            site_df,
            names="Outcome",
            title=f"Success vs Failure for {selected_site}",
        )

        return fig


# Callback for scatter chart
@app.callback(
    Output(
        component_id="success-payload-scatter-chart",
        component_property="figure",
    ),
    [
        Input(
            component_id="site-dropdown",
            component_property="value",
        ),
        Input(
            component_id="payload-slider",
            component_property="value",
        ),
    ],
)
def get_scatter_chart(selected_site, payload_range):

    low, high = payload_range

    # Filter by payload range first
    filtered_df = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= low)
        & (spacex_df["Payload Mass (kg)"] <= high)
    ]

    if selected_site == "ALL":

            fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Correlation between Payload and Success for all Sites",
        )

    else:

        site_df = filtered_df[
            filtered_df["Launch Site"] == selected_site
        ]

        fig = px.scatter(
            site_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=f"Correlation between Payload and Success for {selected_site}",
        )

    return fig


# Run app
if __name__ == "__main__":
    app.run()
