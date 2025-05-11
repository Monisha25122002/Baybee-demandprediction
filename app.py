import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
import plotly.express as px
from prophet.plot import plot_components_plotly

# Streamlit layout
st.set_page_config(layout='wide')
st.title("📈 Baybee - AI Powered Demand Forecasting")

# Load dataset
df = pd.read_csv('baybee_sales_data.csv')

# Sidebar filters
st.sidebar.header("🔍 Filter")
product_option = st.sidebar.selectbox("Select Product", df['Product_Name'].unique())

# Filtered DataFrame
product_df = df[df['Product_Name'] == product_option]
daily_sales = product_df.groupby('Date')['Units_Sold'].sum().reset_index()
daily_sales.columns = ['ds', 'y']
daily_sales['ds'] = pd.to_datetime(daily_sales['ds'])

# Prophet Model
model = Prophet()
model.fit(daily_sales)

# Forecast
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# --- 1. Actual vs Forecasted Sales Line Chart ---
st.subheader(f"📊 Sales Forecast for '{product_option}'")
fig1 = go.Figure()

# Actual Sales
# Filter forecast to show only future dates
last_actual_date = daily_sales['ds'].max()
future_forecast = forecast[forecast['ds'] > last_actual_date]

# Forecast Line (only future)
fig1.add_trace(go.Scatter(x=future_forecast['ds'], y=future_forecast['yhat'],
                          mode='lines', name='Forecasted Sales', line=dict(color='green', dash='dash')))

# Confidence Interval (only future)
fig1.add_trace(go.Scatter(
    x=future_forecast['ds'], y=future_forecast['yhat_upper'],
    line=dict(width=0), mode='lines', name='Upper Bound',
    showlegend=False
))
fig1.add_trace(go.Scatter(
    x=future_forecast['ds'], y=future_forecast['yhat_lower'],
    fill='tonexty', fillcolor='rgba(0,255,0,0.1)',
    line=dict(width=0), mode='lines', name='Lower Bound',
    showlegend=False
))


fig1.update_layout(
    title="🧠 Forecast vs Actual Sales",
    xaxis_title="Date", yaxis_title="Units Sold",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig1, use_container_width=True)

# --- 2. Prophet Forecast Components ---
st.subheader("🔍 Forecast Decomposition (Trend & Seasonality)")
fig2 = plot_components_plotly(model, forecast)
st.plotly_chart(fig2, use_container_width=True)

# --- 3. Monthly Sales Trend ---
st.subheader("📅 Monthly Sales Trend")

monthly_sales = daily_sales.copy()
monthly_sales['Month'] = monthly_sales['ds'].dt.strftime('%b %Y')
monthly_summary = monthly_sales.groupby('Month')['y'].sum().reset_index()

fig3 = px.bar(monthly_summary, x='Month', y='y', text='y',
              labels={'y': 'Total Units Sold', 'Month': 'Month-Year'},
              color='y', color_continuous_scale='Blues')

fig3.update_traces(texttemplate='%{text:.0f}', textposition='outside')
fig3.update_layout(
    title="📦 Total Sales by Month",
    xaxis_tickangle=-45,
    template="plotly_white",
    showlegend=False
)
st.plotly_chart(fig3, use_container_width=True)


# --- Forecast Table ---
st.subheader("📋 Forecast Table (Next 30 Days)")
forecast_table = forecast[['ds', 'yhat']].tail(30).rename(columns={'ds': 'Date', 'yhat': 'Predicted Units Sold'})
st.dataframe(forecast_table)
