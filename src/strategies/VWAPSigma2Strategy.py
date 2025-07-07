import pandas as pd

class VWAPSigma2Strategy:
    def generate_signal(self, df: pd.DataFrame):
        """
        Generate a trading signal based on VWAP and 2-sigma bands.

        Parameters:
            df (pd.DataFrame): DataFrame containing columns 'high', 'low', 'close', and 'volume'.

        Returns:
            str: Trading signal, one of "BUY (VWAP -2σ reversal + 2x volume)", 
                 "SELL (VWAP +2σ reversal + 2x volume)", 
                 "SELL (VWAP +2σ breakdown)", 
                 "BUY (VWAP -2σ breakout)", or "HOLD".
        """
        typical_price = (df["high"] + df["low"] + df["close"]) / 3
        vwap = (typical_price * df["volume"]).cumsum() / df["volume"].cumsum()
        std = typical_price.rolling(window=20).std()
        upper_band = vwap + 2 * std
        lower_band = vwap - 2 * std
        avg_vol = df["volume"].rolling(window=20).mean()
        last_close = df["close"].iloc[-1]
        last_lower = lower_band.iloc[-1]
        last_vwap = vwap.iloc[-1]
        last_vol = df["volume"].iloc[-1]
        last_avg_vol = avg_vol.iloc[-1]

        # Buy logic: Price crosses above lower band (VWAP-2σ) and volume is at least 2x average, and previous bar closed below lower band
        if (
            last_close > last_lower
            and df["close"].iloc[-2] < lower_band.iloc[-2]
            and last_vol >= 2 * last_avg_vol
        ):
            return "BUY (VWAP -2σ reversal + 2x volume)"
        # Sell logic: Price crosses below upper band (VWAP+2σ) and volume is at least 2x average, and previous bar closed above upper band
        elif (
            last_close < upper_band.iloc[-1]
            and df["close"].iloc[-2] > upper_band.iloc[-2]
            and last_vol >= 2 * last_avg_vol
        ):
            return "SELL (VWAP +2σ reversal + 2x volume)"
        elif last_close > upper_band.iloc[-1]:
            return "SELL (VWAP +2σ breakdown)"
        elif last_close < lower_band.iloc[-1]:
            return "BUY (VWAP -2σ breakout)"
        else:
            return "HOLD"

    def backtest(self, df: pd.DataFrame):
        """
        Backtest the VWAP -2σ reversal strategy.

        Parameters:
            df (pd.DataFrame): DataFrame containing columns 'high', 'low', 'close', 'volume', and a datetime column
                               named 'datetime_ist' or 'datetime'. If neither is present, raises ValueError.

        Returns:
            pd.DataFrame: DataFrame of trades with entry/exit info and PnL.
        """
        # Standardize datetime column
        if "datetime_ist" in df.columns:
            datetime_col = "datetime_ist"
        elif "datetime" in df.columns:
            datetime_col = "datetime"
        else:
            raise ValueError("DataFrame must contain a 'datetime_ist' or 'datetime' column.")

        typical_price = (df["high"] + df["low"] + df["close"]) / 3
        vwap = (typical_price * df["volume"]).cumsum() / df["volume"].cumsum()
        std = typical_price.rolling(window=20).std()
        lower_band = vwap - 2 * std
        avg_vol = df["volume"].rolling(window=20).mean()

        position = None
        entry_price = 0
        entry_time = None
        trades = []
        take_profit = 0.0628  # 6.28%
        stop_loss = -0.0314   # -3.14%

        for i in range(20, len(df)):
            close = df["close"].iloc[i]
            prev_close = df["close"].iloc[i-1]
            lb = lower_band.iloc[i]
            prev_lb = lower_band.iloc[i-1]
            vol = df["volume"].iloc[i]
            avgv = avg_vol.iloc[i]
            dt = df[datetime_col].iloc[i]

            # Check for open position and apply TP/SL
            if position == "long":
                change = (close - entry_price) / entry_price
                if change >= take_profit:
                    trades.append({
                        "entry_time": entry_time,
                        "exit_time": dt,
                        "side": "BUY_TP",
                        "entry_price": entry_price,
                        "exit_price": close,
                        "pnl": close - entry_price
                    })
                    position = None
                    entry_price = 0
                    entry_time = None
                elif change <= stop_loss:
                    trades.append({
                        "entry_time": entry_time,
                        "exit_time": dt,
                        "side": "BUY_SL",
                        "entry_price": entry_price,
                        "exit_price": close,
                        "pnl": close - entry_price
                    })
                    position = None
                    entry_price = 0
                    entry_time = None

            # Entry signal (VWAP -2σ reversal + 2x volume)
            if (
                position is None
                and close > lb
                and prev_close < prev_lb
                and vol >= 2 * avgv
            ):
                position = "long"
                entry_price = close
                entry_time = dt

        if position == "long":
            trades.append({
                "entry_time": entry_time,
                "exit_time": df[datetime_col].iloc[-1],
                "side": "BUY_EOD",
                "entry_price": entry_price,
                "exit_price": df["close"].iloc[-1],
                "pnl": df["close"].iloc[-1] - entry_price
            })

        return pd.DataFrame(trades)
