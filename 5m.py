import requests
import pandas as pd
import ta  # technical analysis library


# Parameters
symbol = "BTCUSDT"
interval = "5m"
limit = 1000  # Max = 1000

# Binance endpoint
url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"

# Fetch data
response = requests.get(url)
data = response.json()

# Define columns
columns = [
    "Open Time", "Open Price", "High Price", "Low Price", "Close Price", "Volume",
    "Close Time", "Quote Volume", "Number of Trades",
    "Taker Buy Base Volume", "Taker Buy Quote Volume", "Ignore"
]

# Convert to DataFrame
df = pd.DataFrame(data, columns=columns)

# Format time columns
df["Open Time"] = pd.to_datetime(df["Open Time"], unit='ms')
df["Close Time"] = pd.to_datetime(df["Close Time"], unit='ms')


# Exclude incomplete candle
import time
now_ms = int(time.time() * 1000)
df = df[df["Close Time"].astype('int64') // 10**6 <= now_ms]

# Convert numeric columns
numeric_cols = ["Volume", "Open Price", "High Price", "Low Price", "Close Price"]
df[numeric_cols] = df[numeric_cols].astype(float)








# === Add Technical Indicators ===

# RSI
df["RSI_14"] = ta.momentum.RSIIndicator(close=df["Close Price"], window=14).rsi()

# EMA
df["EMA_14"] = ta.trend.EMAIndicator(close=df["Close Price"], window=14).ema_indicator()

# MACD
macd = ta.trend.MACD(close=df["Close Price"])
df["MACD"] = macd.macd()
df["MACD_Signal"] = macd.macd_signal()
df["MACD_Diff"] = macd.macd_diff()

# Bollinger Bands (20-period)
bb = ta.volatility.BollingerBands(close=df["Close Price"], window=20, window_dev=2)
df["BB_Middle"] = bb.bollinger_mavg()
df["BB_Upper"] = bb.bollinger_hband()
df["BB_Lower"] = bb.bollinger_lband()

# OBV (On-Balance Volume)
df["OBV"] = ta.volume.OnBalanceVolumeIndicator(close=df["Close Price"], volume=df["Volume"]).on_balance_volume()


# ATR
atr = ta.volatility.AverageTrueRange(
    high=df["High Price"],
    low=df["Low Price"],
    close=df["Close Price"],
    window=14
)
df["ATR_14"] = atr.average_true_range()

# Smart Money Concept – Swing Highs/Lows
df["Swing_High"] = (
    (df["High Price"].shift(1) < df["High Price"]) &
    (df["High Price"].shift(-1) < df["High Price"])
)

df["Swing_Low"] = (
    (df["Low Price"].shift(1) > df["Low Price"]) &
    (df["Low Price"].shift(-1) > df["Low Price"])
)







export_columns = [
    "Open Time", "Volume", "Open Price", "High Price", "Low Price", "Close Price",
    "RSI_14", "EMA_14", "MACD", "MACD_Signal", "MACD_Diff",
    "BB_Middle", "BB_Upper", "BB_Lower", "OBV",
    "ATR_14", "Swing_High", "Swing_Low"
]

export_df = df[export_columns]

# === Export to CSV ===
csv_filename = f"{symbol}_{interval}_data.csv"
export_df.to_csv(csv_filename, index=False)

# === Export to Excel ===
excel_filename = f"{symbol}_{interval}_data.xlsx"
export_df.to_excel(excel_filename, index=False)

print(f"✅ Export complete:\n- CSV: {csv_filename}\n- Excel: {excel_filename}")
