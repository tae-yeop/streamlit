# https://www.youtube.com/watch?v=0E_31WqVzCY
import streamlit as st
from datetime import date
# prophet 설치할때 
# pystan을 먼저 설치
# 
# 안되면 conda 명령어로 설치
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go


START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")

stocks = ("AAPL", "GOOG", "MSFT", "GME")
selected_stock = st.sidebar.selectbox("Select dataset for prediction", stocks)
st.write(f"## {selected_stock} Stock")

n_years = st.sidebar.slider("Years of prediction:", 1, 4)
period = n_years * 365

# 다운받은 데이터를 캐쉬해줌
@st.cache
def load_data(ticker):
  data = yf.download(ticker, START, TODAY)
  data.reset_index(inplace=True) # dates를 index column으로 사용
  return data

data_load_state = st.text("Load data...")
data = load_data(selected_stock)
data_load_state.text("Loading data...done!")

st.subheader('Raw data')
# st can handle pd data
st.write(data.tail())

def plot_raw_data():
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
  fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_open'))
  fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
  st.plotly_chart(fig)
  
plot_raw_data()


# Forcasting
df_train = data[['Date', 'Close']]
# fbprophet require certian format
df_train = df_train.rename(columns={"Date" : "ds", "Close":"y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail())

st.write('forecast data')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1) #plotly chart이면 st에서 지원하는 함수를 그대로 사용 

st.write('forecast components')
fig2 = m.plot_components(forecast)
st.write(fig2) #plotly chart가 아니라서 그냥 write를 사용