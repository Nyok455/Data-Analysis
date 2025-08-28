# Professional Petroleum Analytics Dashboard

import dash
from dash import dcc, html, Input, Output, callback_context
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Create sample data for the dashboard (in a real scenario, you would load from databases/APIs)
def create_dashboard_data():
    # Production data
    dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='M')
    production_data = pd.DataFrame({
        'Date': dates,
        'Oil_Production': np.random.lognormal(7.5, 0.3, len(dates)) * 1000,
        'Water_Production': np.random.lognormal(7.2, 0.4, len(dates)) * 1000,
        'Gas_Production': np.random.lognormal(7.0, 0.35, len(dates)) * 10000,
        'Field': ['Field_A'] * 24 + ['Field_B'] * 24 + ['Field_C'] * 24
    })
    
    # Well performance data
    wells = [f'Well_{i:03d}' for i in range(1, 21)]
    well_data = pd.DataFrame({
        'Well': wells * 5,
        'Production': np.random.lognormal(6.5, 0.5, 100) * 1000,
        'Water_Cut': np.random.uniform(0.1, 0.9, 100),
        'GOR': np.random.lognormal(3.5, 0.4, 100),
        'Date': pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365, 100), unit='D')
    })
    
    # Economic data
    economic_data = pd.DataFrame({
        'Scenario': ['Base Case', 'Low Price', 'High Price', 'Cost Reduction', 'Accelerated'],
        'NPV_MM': [450, 220, 780, 520, 380],
        'IRR': [0.22, 0.12, 0.35, 0.28, 0.18],
        'CAPEX_MM': [1200, 1200, 1200, 1000, 1400],
        'Risk_Score': [5.2, 7.8, 3.2, 4.5, 6.1]
    })
    
    # Reservoir properties
    reservoir_data = pd.DataFrame({
        'X': np.random.randint(0, 100, 500),
        'Y': np.random.randint(0, 100, 500),
        'Porosity': np.random.uniform(0.05, 0.35, 500),
        'Permeability': np.random.lognormal(2.5, 0.8, 500),
        'Saturation': np.random.uniform(0.1, 0.9, 500),
        'Facies': np.random.choice(['Sandstone', 'Shale', 'Limestone'], 500, p=[0.6, 0.3, 0.1])
    })
    
    return production_data, well_data, economic_data, reservoir_data

# Create the data
production_data, well_data, economic_data, reservoir_data = create_dashboard_data()

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Petroleum Engineering Analytics Dashboard", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    
    # Filters and controls
    html.Div([
        html.Div([
            html.Label("Select Field:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='field-selector',
                options=[{'label': field, 'value': field} for field in production_data['Field'].unique()],
                value='Field_A',
                clearable=False
            )
        ], style={'width': '24%', 'display': 'inline-block', 'marginRight': '1%'}),
        
        html.Div([
            html.Label("Date Range:", style={'fontWeight': 'bold'}),
            dcc.DatePickerRange(
                id='date-range',
                start_date=production_data['Date'].min(),
                end_date=production_data['Date'].max(),
                display_format='YYYY-MM-DD'
            )
        ], style={'width': '32%', 'display': 'inline-block', 'marginRight': '1%'}),
        
        html.Div([
            html.Label("Production Type:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='production-type',
                options=[
                    {'label': 'Oil', 'value': 'Oil_Production'},
                    {'label': 'Water', 'value': 'Water_Production'},
                    {'label': 'Gas', 'value': 'Gas_Production'}
                ],
                value='Oil_Production',
                clearable=False
            )
        ], style={'width': '24%', 'display': 'inline-block', 'marginRight': '1%'}),
        
        html.Div([
            html.Label("Chart Theme:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='theme-selector',
                options=[
                    {'label': 'Plotly White', 'value': 'plotly_white'},
                    {'label': 'Plotly Dark', 'value': 'plotly_dark'},
                    {'label': 'GGPlot2', 'value': 'ggplot2'}
                ],
                value='plotly_white',
                clearable=False
            )
        ], style={'width': '18%', 'display': 'inline-block'}),
    ], style={'marginBottom': 30, 'padding': 10, 'borderRadius': 5, 'backgroundColor': '#f8f9fa'}),
    
    # First row of charts
    html.Div([
        html.Div([
            dcc.Graph(id='production-trend-chart')
        ], style={'width': '49%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='economic-analysis-chart')
        ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'}),
    ]),
    
    # Second row of charts
    html.Div([
        html.Div([
            dcc.Graph(id='reservoir-properties-chart')
        ], style={'width': '32%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='well-performance-chart')
        ], style={'width': '32%', 'display': 'inline-block', 'marginLeft': '2%'}),
        
        html.Div([
            dcc.Graph(id='forecast-chart')
        ], style={'width': '32%', 'display': 'inline-block', 'marginLeft': '2%'}),
    ], style={'marginTop': 20}),
    
    # Third row of charts
    html.Div([
        html.Div([
            dcc.Graph(id='risk-analysis-chart')
        ], style={'width': '49%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='performance-metrics-chart')
        ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'}),
    ], style={'marginTop': 20}),
    
    # Hidden div to store intermediate values
    html.Div(id='intermediate-data', style={'display': 'none'})
])

# Callback to update all charts based on user input
@app.callback(
    [Output('production-trend-chart', 'figure'),
     Output('economic-analysis-chart', 'figure'),
     Output('reservoir-properties-chart', 'figure'),
     Output('well-performance-chart', 'figure'),
     Output('forecast-chart', 'figure'),
     Output('risk-analysis-chart', 'figure'),
     Output('performance-metrics-chart', 'figure')],
    [Input('field-selector', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('production-type', 'value'),
     Input('theme-selector', 'value')]
)
def update_dashboard(selected_field, start_date, end_date, production_type, theme):
    # Filter data based on user selection
    filtered_production = production_data[
        (production_data['Field'] == selected_field) & 
        (production_data['Date'] >= start_date) & 
        (production_data['Date'] <= end_date)
    ]
    
    # 1. Production Trend Chart
    production_fig = px.line(
        filtered_production, 
        x='Date', 
        y=production_type,
        title=f'{production_type.replace("_", " ")} Trend',
        template=theme
    )
    production_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Production (bbl/day)",
        hovermode='x unified'
    )
    
    # 2. Economic Analysis Chart
    economic_fig = px.bar(
        economic_data,
        x='Scenario',
        y='NPV_MM',
        title='Economic Analysis by Scenario',
        template=theme,
        color='IRR',
        color_continuous_scale='Viridis'
    )
    economic_fig.update_layout(
        xaxis_title="Scenario",
        yaxis_title="NPV ($MM)"
    )
    
    # 3. Reservoir Properties Chart
    reservoir_fig = px.scatter(
        reservoir_data,
        x='X',
        y='Y',
        color='Porosity',
        size='Permeability',
        title='Reservoir Properties Distribution',
        template=theme,
        hover_data=['Saturation', 'Facies']
    )
    reservoir_fig.update_layout(
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate"
    )
    
    # 4. Well Performance Chart
    well_fig = px.box(
        well_data,
        x='Well',
        y='Production',
        title='Well Production Distribution',
        template=theme
    )
    well_fig.update_layout(
        xaxis_title="Well",
        yaxis_title="Production (bbl/day)",
        xaxis_tickangle=-45
    )
    
    # 5. Forecast Chart
    # Create a simple forecast based on historical data
    forecast_dates = pd.date_range(
        start=filtered_production['Date'].max() + timedelta(days=30),
        periods=12,
        freq='M'
    )
    
    last_value = filtered_production[production_type].iloc[-1]
    forecast_values = [last_value * (0.97 ** i) for i in range(12)]
    
    forecast_df = pd.DataFrame({
        'Date': forecast_dates,
        'Production': forecast_values,
        'Type': ['Forecast'] * 12
    })
    
    historical_df = pd.DataFrame({
        'Date': filtered_production['Date'],
        'Production': filtered_production[production_type],
        'Type': ['Historical'] * len(filtered_production)
    })
    
    combined_df = pd.concat([historical_df, forecast_df])
    
    forecast_fig = px.line(
        combined_df,
        x='Date',
        y='Production',
        color='Type',
        title='Production Forecast',
        template=theme
    )
    forecast_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Production (bbl/day)"
    )
    
    # 6. Risk Analysis Chart
    risk_fig = go.Figure()
    
    risk_fig.add_trace(go.Scatterpolar(
        r=economic_data['Risk_Score'],
        theta=economic_data['Scenario'],
        fill='toself',
        name='Risk Score'
    ))
    
    risk_fig.update_layout(
        title='Risk Analysis by Scenario',
        template=theme,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=False
    )
    
    # 7. Performance Metrics Chart
    metrics_data = well_data.groupby('Well').agg({
        'Production': 'mean',
        'Water_Cut': 'mean',
        'GOR': 'mean'
    }).reset_index()
    
    metrics_fig = px.scatter_matrix(
        metrics_data,
        dimensions=['Production', 'Water_Cut', 'GOR'],
        title='Well Performance Metrics',
        template=theme,
        color='Production',
        hover_name='Well'
    )
    
    return production_fig, economic_fig, reservoir_fig, well_fig, forecast_fig, risk_fig, metrics_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)