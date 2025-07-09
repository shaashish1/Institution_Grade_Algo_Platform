import pandas as pd

class FiftyTwoWeekLowStrategy:
    def generate_signal(self, df: pd.DataFrame):
        # Assumes df has a 'close' column and at least 252 rows (1 year of trading days)
        if len(df) < 252:
            return "NOT ENOUGH DATA"
        last_close = df["close"].iloc[-1]
        min_52w = df["close"].iloc[-252:].min()
        if last_close <= min_52w:
            return "BUY (52-week low breakout)"
        else:
            return "HOLD"
