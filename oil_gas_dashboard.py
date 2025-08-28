import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server


# Generate sample data
def generate_data():
    # Operator data
    operators = ['Operator 1', 'Operator 2']

    # Generate production data for oil and gas
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='W')

    production_data = []
    for date in dates:
        for operator in operators:
            oil_current = np.random.randint(150000, 200000)
            oil_previous = oil_current * np.random.uniform(0.85, 1.15)
            oil_change = ((oil_current - oil_previous) / oil_previous) * 100

            gas_current = np.random.randint(120000, 180000)
            gas_previous = gas_current * np.random.uniform(0.85, 1.15)
            gas_change = ((gas_current - gas_previous) / gas_previous) * 100

            production_data.append({
                'Date': date,
                'Operator': operator,
                'Oil_Current': oil_current,
                'Oil_Previous': oil_previous,
                'Oil_Change': oil_change,
                'Gas_Current': gas_current,
                'Gas_Previous': gas_previous,
                'Gas_Change': gas_change
            })

    production_df = pd.DataFrame(production_data)

    # Generate state production data
    states = ['California', 'Texas', 'Oklahoma', 'Louisiana', 'Alaska', 'North Dakota']
    state_data = []

    for i in range(6):  # Last 6 weeks
        week_date = dates[-i - 1]
        for state in states:
            production = np.random.randint(50000, 200000)
            state_data.append({
                'Week': f'Week {i + 1}',
                'Date': week_date,
                'State': state,
                'Production': production
            })

    state_df = pd.DataFrame(state_data)

    # Generate well data
    wells = [f'Well-{i}' for i in range(1, 61)]
    well_data = []

    for well in wells:
        oil_produced = np.random.randint(8000, 15000)
        oil_target = oil_produced * np.random.uniform(1.1, 1.3)

        gas_produced = np.random.randint(8000, 15000)
        gas_target = gas_produced * np.random.uniform(1.1, 1.3)

        well_data.append({
            'Well': well,
            'Oil_Produced': oil_produced,
            'Oil_Target': oil_target,
            'Gas_Produced': gas_produced,
            'Gas_Target': gas_target
        })

    well_df = pd.DataFrame(well_data)

    return production_df, state_df, well_df


# Generate the data
production_data, state_data, well_data = generate_data()

# Get the latest data for the dashboard
latest_date = production_data['Date'].max()
latest_production = production_data[production_data['Date'] == latest_date]

# Get top 3 oil and gas wells
top_oil_wells = well_data.nlargest(3, 'Oil_Produced')
top_gas_wells = well_data.nlargest(3, 'Gas_Produced')

# Create the app layout
app.layout = html.Div([
    html.H1("Oil and Gas Production Monitoring Dashboard",
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),

    # Operator KPIs
    html.Div([
        html.Div([
            html.H3("Operator 1", style={'textAlign': 'center'}),
            html.Div([
                html.Div([
                    html.H4("Oil", style={'textAlign': 'center', 'color': '#e74c3c'}),
                    html.H5(
                        f"{latest_production[latest_production['Operator'] == 'Operator 1']['Oil_Change'].values[0]:.1f}%",
                        style={'textAlign': 'center', 'color': '#e74c3c'}),
                    html.P(
                        f"Current week {latest_production[latest_production['Operator'] == 'Operator 1']['Oil_Current'].values[0]:,.0f} bbl",
                        style={'textAlign': 'center', 'marginBottom': '5px'}),
                    html.P(
                        f"Previous week {latest_production[latest_production['Operator'] == 'Operator 1']['Oil_Previous'].values[0]:,.0f} bbl",
                        style={'textAlign': 'center', 'marginTop': '0px', 'color': '#7f8c8d'})
                ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px',
                          'borderRight': '1px solid #ecf0f1'}),

                html.Div([
                    html.H4("Gas", style={'textAlign': 'center', 'color': '#3498db'}),
                    html.H5(
                        f"{latest_production[latest_production['Operator'] == 'Operator 1']['Gas_Change'].values[0]:.1f}%",
                        style={'textAlign': 'center', 'color': '#3498db'}),
                    html.P(
                        f"Current week {latest_production[latest_production['Operator'] == 'Operator 1']['Gas_Current'].values[0]:,.0f} bbl",
                        style={'textAlign': 'center', 'marginBottom': '5px'}),
                    html.P(
                        f"Previous week {latest_production[latest_production['Operator'] == 'Operator 1']['Gas_Previous'].values[0]:,.0f} bbl",
                        style={'textAlign': 'center', 'marginTop': '0px', 'color': '#7f8c8d'})
                ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'float': 'right'})
            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '5px'})
        ], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            html.H3("Operator 2", style={'textAlign': 'center'}),
            html.Div([
                html.Div([
                    html.H4("Oil", style={'textAlign': 'center', 'color': '#e74c3c'}),
                    html.H5(
                        f"{latest_production[latest_production['Operator'] == 'Operator 2']['Oil_Change'].values[0]:.1f}%",
                        style={'textAlign': 'center', 'color': '#e74c3c'}),
                    html.P(
                        f"Current week {latest_production[latest_production['Operator'] == 'Operator 2']['Oil_Current'].values[0]:,.0f} bbl",
                        style={'textAlign': 'center', 'marginBottom': '5px'}),
                    html.P(
                        f"Previous week {latest_production[latest_production['Operator'] == 'Operator 2']['Oil_Previous'].values[0]:,.0f} bbl",
                        style={'textAlign': 'center', 'marginTop': '0px', 'color': '#7f8c8d'})
                ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px',
                          'borderRight': '1px solid #ecf0f1'}),

                html.Div([
                    html.H4("Gas", style={'textAlign': 'center', 'color': '#3498db'}),
                    html.H5(
                        f"{latest_production[latest_production['Operator'] == 'Operator 2']['Gas_Change'].values[0]:.1f}%",
                        style={'textAlign': 'center', 'color': '#3498db'}),
                    html.P(
                        f"Current week {latest_production[latest_production['Operator'] == 'Operator 2']['Gas_Current'].values[0]:,.0f} bbl",
                        style={'textAlign': 'center', 'marginBottom': '5px'}),
                    html.P(
                        f"Previous week {latest_production[latest_production['Operator'] == 'Operator 2']['Gas_Previous'].values[0]:,.0f} bbl",
                        style={'textAlign': 'center', 'marginTop': '0px', 'color': '#7f8c8d'})
                ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'float': 'right'})
            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '5px'})
        ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'})
    ], style={'marginBottom': 30}),

    # Charts row
    html.Div([
        # Production by State chart
        html.Div([
            html.H3("Production by State in Last 6 Weeks", style={'textAlign': 'center'}),
            dcc.Graph(
                id='state-production-chart',
                figure=px.bar(
                    state_data,
                    x='Week',
                    y='Production',
                    color='State',
                    title='Production by State',
                    barmode='group'
                ).update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='#f8f9fa',
                    showlegend=True
                )
            )
        ], style={'width': '49%', 'display': 'inline-block'}),

        # Top wells charts
        html.Div([
            html.Div([
                html.H4("Top 3 Oil Producing Wells", style={'textAlign': 'center', 'color': '#e74c3c'}),
                dcc.Graph(
                    id='top-oil-wells',
                    figure={
                        'data': [
                            go.Bar(
                                name='Produced',
                                x=top_oil_wells['Well'],
                                y=top_oil_wells['Oil_Produced'],
                                marker_color='#e74c3c'
                            ),
                            go.Bar(
                                name='Target',
                                x=top_oil_wells['Well'],
                                y=top_oil_wells['Oil_Target'],
                                marker_color='#f1948a'
                            )
                        ],
                        'layout': go.Layout(
                            barmode='group',
                            plot_bgcolor='white',
                            paper_bgcolor='#f8f9fa',
                            showlegend=True,
                            yaxis_title='Production (bbl)'
                        )
                    }
                )
            ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                html.H4("Top 3 Gas Producing Wells", style={'textAlign': 'center', 'color': '#3498db'}),
                dcc.Graph(
                    id='top-gas-wells',
                    figure={
                        'data': [
                            go.Bar(
                                name='Produced',
                                x=top_gas_wells['Well'],
                                y=top_gas_wells['Gas_Produced'],
                                marker_color='#3498db'
                            ),
                            go.Bar(
                                name='Target',
                                x=top_gas_wells['Well'],
                                y=top_gas_wells['Gas_Target'],
                                marker_color='#85c1e9'
                            )
                        ],
                        'layout': go.Layout(
                            barmode='group',
                            plot_bgcolor='white',
                            paper_bgcolor='#f8f9fa',
                            showlegend=True,
                            yaxis_title='Production (bbl)'
                        )
                    }
                )
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'})
    ]),

    # Time series chart
    html.Div([
        html.H3("Production Trend Over Time", style={'textAlign': 'center', 'marginTop': '30px'}),
        dcc.Dropdown(
            id='production-type-selector',
            options=[
                {'label': 'Oil', 'value': 'Oil_Current'},
                {'label': 'Gas', 'value': 'Gas_Current'}
            ],
            value='Oil_Current',
            style={'width': '200px', 'margin': '0 auto'}
        ),
        dcc.Graph(id='production-trend-chart')
    ], style={'marginTop': 30, 'padding': '10px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),

    # Footer
    html.Div([
        html.P("Data updated: " + datetime.now().strftime("%Y-%m-%d %H:%M"),
               style={'textAlign': 'center', 'color': '#7f8c8d', 'marginTop': '30px'})
    ])
])


# Callback for the production trend chart
@app.callback(
    Output('production-trend-chart', 'figure'),
    [Input('production-type-selector', 'value')]
)
def update_production_chart(production_type):
    fig = px.line(
        production_data,
        x='Date',
        y=production_type,
        color='Operator',
        title=f'{production_type.split("_")[0]} Production Trend'
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='#f8f9fa',
        yaxis_title='Production (bbl)'
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)