import requests
import json
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Function to fetch historical cryptocurrency data from Binance API
def get_binance_data(symbol, start_date, end_date):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d"

    start_date = datetime.combine(start_date, datetime.min.time())  # Convert date to datetime
    url += f"&startTime={int(start_date.timestamp()) * 1000}"

    end_date = datetime.combine(end_date, datetime.max.time())  # Convert date to datetime
    url += f"&endTime={int(end_date.timestamp()) * 1000}"

    response = requests.get(url)

    if response.status_code == 200:
        klines = json.loads(response.text)
        df = pd.DataFrame(klines, columns=[
            "Open Time", "Open", "High", "Low", "Close", "Volume",
            "Close Time", "Quote Asset Volume", "Number of Trades",
            "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"
        ])
        df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
        df["Close Time"] = pd.to_datetime(df["Close Time"], unit="ms")
        df.set_index("Open Time", inplace=True)
        return df
    else:
        st.error(f"Error: {response.status_code}")

# Streamlit app
st.title(":orange[Crypto Currency Visualization App]")

# Sidebar for user input
st.sidebar.header(':blue[Input Values]', divider='rainbow')

# Get a list of available cryptocurrency symbols
crypto_symbols = [
    'BTCUSDT', 'ETHUSDT', 'LTCUSDT', 'XRPUSDT', 'BCHUSDT', 'ADAUSDT',
    'DOTUSDT', 'LINKUSDT', 'XLMUSDT', 'USDTUSDT', 'BNBUSDT', 'DOGEUSDT',
    'UNIUSDT', 'USDCUSDT', 'EOSUSDT', 'TRXUSDT', 'XMRUSDT', 'XTZUSDT',
    'ATOMUSDT', 'VETUSDT', 'DASHUSDT', 'MIOTAUSDT', 'NEOUSDT', 'MKRUSDT'
]

# Select cryptocurrency using a dropdown menu
crypto_symbol = st.sidebar.selectbox('Select Cryptocurrency :', crypto_symbols, index=0)

# Select date range
start_date_default = datetime.now() - timedelta(days=30)
start_date = st.sidebar.date_input('Start Date', value=start_date_default)
end_date = st.sidebar.date_input('End Date', value=datetime.now())

# Fetch day-wise data from Binance API
crypto_data = get_binance_data(crypto_symbol, start_date, end_date)

# Allow user to pick the number of rows to display
num_rows = st.sidebar.slider('Select the number of rows to display:', min_value=1, max_value=len(crypto_data), value=5)

# Display the selected number of rows
#st.write(f'**:green[{crypto_symbol} Historical Data (OHLC) (Top {num_rows} rows)]**')
#st.write(crypto_data.head(num_rows))
# Display the selected number of rows in descending order
st.write(f'**:green[{crypto_symbol} Historical Data (OHLC) (Top {num_rows} rows)]**')
st.write(crypto_data.sort_index(ascending=False).head(num_rows))

# Line chart with Open, High, Low, and Close prices
line_chart_ohlc = go.Figure()

line_chart_ohlc.add_trace(go.Scatter(x=crypto_data.index, y=crypto_data['Open'], mode='lines', name='Open'))
line_chart_ohlc.add_trace(go.Scatter(x=crypto_data.index, y=crypto_data['High'], mode='lines', name='High'))
line_chart_ohlc.add_trace(go.Scatter(x=crypto_data.index, y=crypto_data['Low'], mode='lines', name='Low'))
line_chart_ohlc.add_trace(go.Scatter(x=crypto_data.index, y=crypto_data['Close'], mode='lines', name='Close'))

line_chart_ohlc.update_layout(
    xaxis_title='Date',
    yaxis_title='Price (USD)',
    title=dict(text=f'{crypto_symbol} OHLC Prices Over Time', font=dict(color='green')),
)

# Candlestick chart
candlestick_chart = go.Figure(data=[go.Candlestick(
    x=crypto_data.index,
    open=crypto_data['Open'],
    high=crypto_data['High'],
    low=crypto_data['Low'],
    close=crypto_data['Close']
)])

candlestick_chart.update_layout(xaxis_title='Date', yaxis_title='Price (USD)',
                                title=dict(text=f'{crypto_symbol} Candlestick Chart', font=dict(color='green')),)

# Display both charts
st.plotly_chart(line_chart_ohlc)
st.plotly_chart(candlestick_chart)