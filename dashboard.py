# petroleum_dashboard.py
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server


# Function to load and process data from your CSV files
def load_data():
    # Initialize empty DataFrames with different names to avoid shadowing
    well_df = pd.DataFrame()
    production_df = pd.DataFrame()
    portfolio_df = pd.DataFrame()
    economic_df = pd.DataFrame()

    # Try to load each CSV file with error handling
    try:
        well_df = pd.read_csv('advanced_well_analysis.csv')
        print("Well data loaded successfully")
    except FileNotFoundError:
        print("Well data file not found. Using sample data.")
        # Create sample well data
        depth = np.arange(1500, 2500, 5)
        well_df = pd.DataFrame({
            'DEPTH': depth,
            'GR': 40 + 100 * np.exp(-(depth - 2000) ** 2 / 100000) + np.random.normal(0, 5, len(depth)),
            'RT': 20 + 80 * np.exp(-(depth - 2200) ** 2 / 80000) + np.random.normal(0, 2, len(depth)),
            'NPHI': 0.3 - 0.2 * np.exp(-(depth - 2100) ** 2 / 90000) + np.random.normal(0, 0.02, len(depth)),
            'RHOB': 2.0 + 0.8 * np.exp(-(depth - 1900) ** 2 / 70000) + np.random.normal(0, 0.05, len(depth)),
            'LITHOLOGY': np.random.choice(['SHALE', 'SANDSTONE', 'LIMESTONE'], len(depth), p=[0.4, 0.4, 0.2]),
            'WELL': 'Sample_Well'
        })

    try:
        production_df = pd.read_csv('advanced_production_data.csv')
        production_df['DATE'] = pd.to_datetime(production_df['DATE'])
        print("Production data loaded successfully")
    except FileNotFoundError:
        print("Production data file not found. Using sample data.")
        # Create sample production data
        dates = pd.date_range(start='2020-01-01', periods=36, freq='M')
        production_df = pd.DataFrame({
            'DATE': dates,
            'OIL_RATE': 1000 * np.exp(-0.03 * np.arange(36)) * np.random.normal(1, 0.1, 36),
            'WATER_RATE': 500 * (1 + 0.02 * np.arange(36)) * np.random.normal(1, 0.1, 36),
            'WATER_CUT': np.linspace(0.1, 0.7, 36) * np.random.normal(1, 0.05, 36),
            'WELL': 'Sample_Well'
        })

    try:
        portfolio_df = pd.read_csv('project_portfolio.csv')
        print("Portfolio data loaded successfully")
    except FileNotFoundError:
        print("Portfolio data file not found. Using sample data.")
        # Create sample portfolio data
        portfolio_df = pd.DataFrame({
            'Project_ID': [f'P{i:03d}' for i in range(1, 11)],
            'Project_Type': np.random.choice(['Exploration', 'Development', 'Enhanced Recovery'], 10),
            'Success_Probability': np.random.uniform(0.3, 0.9, 10),
            'CAPEX_MM': np.random.lognormal(7.5, 0.4, 10),
            'NPV_MM': np.random.normal(500, 200, 10),
            'IRR': np.random.uniform(0.1, 0.4, 10)
        })

    try:
        economic_df = pd.read_csv('economic_analysis_results.csv')
        print("Economic data loaded successfully")
    except FileNotFoundError:
        print("Economic data file not found. Using sample data.")
        # Create sample economic data
        economic_df = pd.DataFrame({
            'Scenario': ['Base Case', 'Low Price', 'High Price', 'Cost Reduction'],
            'NPV_MM': [450, 220, 780, 520],
            'IRR': [0.22, 0.12, 0.35, 0.28],
            'CAPEX_MM': [1200, 1200, 1200, 1000],
            'Risk_Score': [5.2, 7.8, 3.2, 4.5]
        })

    return well_df, production_df, portfolio_df, economic_df


# Load the data
well_data, production_data, portfolio_data, economic_data = load_data()

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Petroleum Engineering Analytics Dashboard",
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),

    # Filters and controls
    html.Div([
        html.Div([
            html.Label("Select Well:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='well-selector',
                options=[{'label': well, 'value': well} for well in well_data['WELL'].unique()],
                value=well_data['WELL'].iloc[0] if 'WELL' in well_data.columns else 'Sample_Well',
                clearable=False
            )
        ], style={'width': '24%', 'display': 'inline-block', 'marginRight': '1%'}),

        html.Div([
            html.Label("Date Range:", style={'fontWeight': 'bold'}),
            dcc.DatePickerRange(
                id='date-range',
                start_date=production_data['DATE'].min() if not production_data.empty else datetime(2020, 1, 1),
                end_date=production_data['DATE'].max() if not production_data.empty else datetime(2022, 12, 31),
                display_format='YYYY-MM-DD'
            )
        ], style={'width': '32%', 'display': 'inline-block', 'marginRight': '1%'}),

        html.Div([
            html.Label("Production Type:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='production-type',
                options=[
                    {'label': 'Oil', 'value': 'OIL_RATE'},
                    {'label': 'Water', 'value': 'WATER_RATE'},
                    {'label': 'Water Cut', 'value': 'WATER_CUT'}
                ],
                value='OIL_RATE',
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
            dcc.Graph(id='well-log-chart')
        ], style={'width': '32%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='portfolio-analysis-chart')
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
])


# Callback to update all charts based on user input
@app.callback(
    [Output('production-trend-chart', 'figure'),
     Output('economic-analysis-chart', 'figure'),
     Output('well-log-chart', 'figure'),
     Output('portfolio-analysis-chart', 'figure'),
     Output('forecast-chart', 'figure'),
     Output('risk-analysis-chart', 'figure'),
     Output('performance-metrics-chart', 'figure')],
    [Input('well-selector', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('production-type', 'value'),
     Input('theme-selector', 'value')]
)
def update_dashboard(selected_well, start_date, end_date, production_type, theme):
    # Filter data based on user selection
    filtered_production = production_data[
        (production_data['WELL'] == selected_well) &
        (production_data['DATE'] >= start_date) &
        (production_data['DATE'] <= end_date)
        ] if not production_data.empty else pd.DataFrame()

    filtered_well = well_data[well_data['WELL'] == selected_well] if not well_data.empty else pd.DataFrame()

    # 1. Production Trend Chart
    if not filtered_production.empty:
        production_fig = px.line(
            filtered_production,
            x='DATE',
            y=production_type,
            title=f'{production_type.replace("_", " ")} Trend for {selected_well}',
            template=theme
        )
    else:
        production_fig = go.Figure()
        production_fig.update_layout(
            title="No production data available",
            template=theme,
            xaxis_title="Date",
            yaxis_title="Production"
        )

    production_fig.update_layout(
        xaxis_title="Date",
        yaxis_title=production_type.replace("_", " "),
        hovermode='x unified'
    )

    # 2. Economic Analysis Chart
    if not economic_data.empty:
        economic_fig = px.bar(
            economic_data,
            x='Scenario',
            y='NPV_MM',
            title='Economic Analysis by Scenario',
            template=theme,
            color='IRR',
            color_continuous_scale='Viridis'
        )
    else:
        economic_fig = go.Figure()
        economic_fig.update_layout(
            title="No economic data available",
            template=theme,
            xaxis_title="Scenario",
            yaxis_title="NPV ($MM)"
        )

    economic_fig.update_layout(
        xaxis_title="Scenario",
        yaxis_title="NPV ($MM)"
    )

    # 3. Well Log Chart
    if not filtered_well.empty:
        well_log_fig = go.Figure()

        # Add well log curves
        if 'GR' in filtered_well.columns:
            well_log_fig.add_trace(go.Scatter(
                x=filtered_well['GR'],
                y=filtered_well['DEPTH'],
                name='Gamma Ray',
                line=dict(color='green')
            ))

        if 'RT' in filtered_well.columns:
            well_log_fig.add_trace(go.Scatter(
                x=filtered_well['RT'],
                y=filtered_well['DEPTH'],
                name='Resistivity',
                line=dict(color='blue'),
                xaxis='x2'
            ))

        if 'NPHI' in filtered_well.columns:
            well_log_fig.add_trace(go.Scatter(
                x=filtered_well['NPHI'],
                y=filtered_well['DEPTH'],
                name='Neutron Porosity',
                line=dict(color='red'),
                xaxis='x3'
            ))

        if 'RHOB' in filtered_well.columns:
            well_log_fig.add_trace(go.Scatter(
                x=filtered_well['RHOB'],
                y=filtered_well['DEPTH'],
                name='Density',
                line=dict(color='orange'),
                xaxis='x4'
            ))

        well_log_fig.update_layout(
            title=f'Well Logs for {selected_well}',
            template=theme,
            yaxis=dict(title='Depth', autorange='reversed'),
            xaxis=dict(title='GR (API)', domain=[0, 0.2]),
            xaxis2=dict(title='RT (ohm-m)', domain=[0.25, 0.45], type='log'),
            xaxis3=dict(title='NPHI (v/v)', domain=[0.5, 0.7]),
            xaxis4=dict(title='RHOB (g/cc)', domain=[0.75, 0.95]),
            showlegend=True
        )
    else:
        well_log_fig = go.Figure()
        well_log_fig.update_layout(
            title="No well log data available",
            template=theme
        )

    # 4. Portfolio Analysis Chart
    if not portfolio_data.empty:
        portfolio_fig = px.scatter(
            portfolio_data,
            x='CAPEX_MM',
            y='NPV_MM',
            size='IRR',
            color='Project_Type',
            title='Project Portfolio Analysis',
            template=theme,
            hover_name='Project_ID'
        )
    else:
        portfolio_fig = go.Figure()
        portfolio_fig.update_layout(
            title="No portfolio data available",
            template=theme,
            xaxis_title="CAPEX ($MM)",
            yaxis_title="NPV ($MM)"
        )

    portfolio_fig.update_layout(
        xaxis_title="CAPEX ($MM)",
        yaxis_title="NPV ($MM)"
    )

    # 5. Forecast Chart
    if not filtered_production.empty and production_type in filtered_production.columns:
        # Create a simple forecast based on historical data
        forecast_dates = pd.date_range(
            start=filtered_production['DATE'].max() + timedelta(days=30),
            periods=12,
            freq='M'
        )

        last_value = filtered_production[production_type].iloc[-1]
        forecast_values = [last_value * (0.97 ** i) for i in range(12)]

        forecast_df = pd.DataFrame({
            'DATE': forecast_dates,
            production_type: forecast_values,
            'Type': ['Forecast'] * 12
        })

        historical_df = pd.DataFrame({
            'DATE': filtered_production['DATE'],
            production_type: filtered_production[production_type],
            'Type': ['Historical'] * len(filtered_production)
        })

        combined_df = pd.concat([historical_df, forecast_df])

        forecast_fig = px.line(
            combined_df,
            x='DATE',
            y=production_type,
            color='Type',
            title=f'Production Forecast for {selected_well}',
            template=theme
        )
    else:
        forecast_fig = go.Figure()
        forecast_fig.update_layout(
            title="No data available for forecasting",
            template=theme,
            xaxis_title="Date",
            yaxis_title="Production"
        )

    forecast_fig.update_layout(
        xaxis_title="Date",
        yaxis_title=production_type.replace("_", " ")
    )

    # 6. Risk Analysis Chart
    if not economic_data.empty:
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
    else:
        risk_fig = go.Figure()
        risk_fig.update_layout(
            title="No risk data available",
            template=theme
        )

    # 7. Performance Metrics Chart
    if not production_data.empty:
        metrics_data = production_data.groupby('WELL').agg({
            'OIL_RATE': 'mean',
            'WATER_RATE': 'mean',
            'WATER_CUT': 'mean'
        }).reset_index()

        metrics_fig = px.scatter_matrix(
            metrics_data,
            dimensions=['OIL_RATE', 'WATER_RATE', 'WATER_CUT'],
            title='Well Performance Metrics',
            template=theme,
            color='OIL_RATE',
            hover_name='WELL'
        )
    else:
        metrics_fig = go.Figure()
        metrics_fig.update_layout(
            title="No performance data available",
            template=theme
        )

    return production_fig, economic_fig, well_log_fig, portfolio_fig, forecast_fig, risk_fig, metrics_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)